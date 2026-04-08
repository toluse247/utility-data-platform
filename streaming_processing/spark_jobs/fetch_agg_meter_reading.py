import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, month, year, current_date
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, to_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType, TimestampType


# -----------------------------
# Configuration
# ----------------------------
S3_BUCKET = os.getenv("S3_BUCKET", "utility-data-bucket")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin1234")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_DB = "utility_db"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin1234"
POSTGRES_TABLE = "monthly_meter_readings"

# -----------------------------
# Initialize SparkSession
# -----------------------------

spark = SparkSession.builder \
    .appName("FetchLatestReadingPerMonth") \
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID) \
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
            "org.postgresql:postgresql:42.7.3") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.access.key", "minioadmin")
hadoop_conf.set("fs.s3a.secret.key", "minioadmin")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")

# ----------------------------
# Create schema for reading CSV
# ----------------------------
schema = StructType([
    StructField("meter_reading_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("meter_number", StringType(), True),
    StructField("read_timestamp", TimestampType(), True),
    StructField("meter_reading", DoubleType(), True),
    StructField("year", IntegerType(), True),
    StructField("month", IntegerType(), True),
    StructField("day", IntegerType(), True),
    StructField("hour", IntegerType(), True)
])

# ----------------------------
# Read from S3
# ----------------------------
df = spark.read \
    .option("header", True) \
    .option("recursiveFileLookup", "true") \
    .schema(schema) \
    .csv("s3a://utility-data-bucket/meter_readings/")

print("Data read from S3:")
df.show(5)
# -----------------------------
# Cast columns properly
# -----------------------------
df = df.withColumn("read_timestamp", to_timestamp(col("read_timestamp"))) \
       .withColumn("meter_reading", col("meter_reading").cast("double")) \
       .withColumn("customer_id", col("customer_id").cast("int"))

print("Columns properly casted")

# ------------------------------------------
# Get latest reading per customer per month
# ------------------------------------------
window_spec = Window.partitionBy("customer_id", "year", "month") \
                    .orderBy(col("read_timestamp").desc())

df_latest = df.withColumn("rank", row_number().over(window_spec)) \
              .filter(col("rank") == 1) \
              .drop("rank")

print("Latest reading per customer per month:")
df_latest.show(5)

# -----------------------------
# Select required columns
# -----------------------------
df_final = df_latest.select(
    "customer_id",
    "year",
    "month",
    "meter_reading"
)

print("Final DataFrame to write to Postgres:")
df_final.show(5)
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
