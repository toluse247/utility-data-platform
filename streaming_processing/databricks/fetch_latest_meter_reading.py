from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, month, year, current_date
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, to_timestamp

# -----------------------------
# Configuration
# -----------------------------
CASSANDRA_HOST = "localhost"
CASSANDRA_KEYSPACE = "utility_db"
CASSANDRA_TABLE = "payments"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "utility_db"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = "admin1234"
POSTGRES_TABLE = "customer_monthly_payments"

# -----------------------------
# Initialize SparkSession
# -----------------------------
spark = SparkSession.builder \
    .appName("GetLatestReadingPerMonth") \
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

# -----------------------------
# Extract year and month
# -----------------------------

df = df.withColumn("year", year(col("read_timestamp"))) \
       .withColumn("month", month(col("read_timestamp")))

# ------------------------------------------
# Get latest reading per customer per month
# ------------------------------------------
window_spec = Window.partitionBy("customer_id", "year", "month") \
                    .orderBy(col("read_timestamp").desc())

df_latest = df.withColumn("rank", row_number().over(window_spec)) \
              .filter(col("rank") == 1) \
              .drop("rank")

# -----------------------------
# Select required columns
# -----------------------------
df_final = df_latest.select(
    "customer_id",
    "year",
    "month",
    "meter_reading",
    "read_timestamp"
)

# -----------------------------
# Write to Postgres Table
# -----------------------------

df_final.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/utility_db") \
    .option("dbtable", "monthly_latest_meter_reading") \
    .option("user", "admin") \
    .option("password", "admin123") \
    .mode("append") \
    .save()
