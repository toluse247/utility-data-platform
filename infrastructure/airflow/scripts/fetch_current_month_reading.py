import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import add_months, col, sum as _sum, month, year, current_date
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, to_timestamp

# -----------------------------
# Configuration
# ----------------------------
S3_BUCKET = os.getenv("S3_BUCKET", "utility-data-bucket")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "utility_db"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin1234"
POSTGRES_TABLE = "stg_present_readings"

# -----------------------------
# Initialize SparkSession
# -----------------------------

spark = SparkSession.builder \
    .appName("GetLatestReadingCurrentMonth") \
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID) \
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
            "org.postgresql:postgresql:42.7.3") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# ----------------------------
# Read from S3
# ----------------------------
df = spark.read \
    .option("header", True) \
    .csv("s3a://utility-data-bucket/meter_readings/")

# -----------------------------
# Cast columns properly
# -----------------------------
df = df.withColumn("read_timestamp", to_timestamp(col("read_timestamp"))) \
       .withColumn("meter_reading", col("meter_reading").cast("double")) \
       .withColumn("customer_id", col("customer_id").cast("int"))

# ------------------------------------------
# Filter readings for the current month
# ------------------------------------------
df_current = df.filter(
    (month(col("read_timestamp")) == month(add_months(current_date(), -1))) &
    (year(col("read_timestamp")) == year(add_months(current_date(), -1)))
)

# -----------------------------
# Extract year and month
# -----------------------------

df_current = df_current.withColumn("year", year(col("read_timestamp"))) \
       .withColumn("month", month(col("read_timestamp")))

# ------------------------------------------
# Get latest reading per customer
# ------------------------------------------
window_spec = Window.partitionBy("customer_id") \
                    .orderBy(col("read_timestamp").desc())

df_latest = df_current.withColumn("rank", row_number().over(window_spec)) \
              .filter(col("rank") == 1) \
              .drop("rank")

# -----------------------------
# Select required columns
# -----------------------------
df_final = df_latest.select(
    "customer_id",
    "year",
    "month",
    "meter_reading"
)

# -----------------------------
# Write to Postgres Table
# -----------------------------
df_final.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") \
    .option("dbtable", POSTGRES_TABLE) \
    .option("user", POSTGRES_USER) \
    .option("password", POSTGRES_PASSWORD) \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

spark.stop()
