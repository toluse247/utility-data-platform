from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, month, year, current_date
from pyspark.sql.types import TimestampType

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
    .appName("AggregatePaymentsCurrentMonth") \
    .config("spark.cassandra.connection.host", CASSANDRA_HOST) \
    .getOrCreate()

# -----------------------------
# Load payments from Cassandra
# -----------------------------
df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table=CASSANDRA_TABLE, keyspace=CASSANDRA_KEYSPACE) \
    .load()

# -------------------------
# Ensure timestamp is proper type
# -------------------------
df = df.withColumn(
    "payment_timestamp",
    col("payment_timestamp").cast(TimestampType())
)

# -----------------------------
# Filter for current month only
# -----------------------------
df_current = df.filter(
    (month(col("payment_timestamp")) == month(current_date())) &
    (year(col("payment_timestamp")) == year(current_date()))
)

# -------------------------
# Extract year & month
# -------------------------
df_current = df_current.withColumn("year", year(col("payment_timestamp"))) \
       .withColumn("month", month(col("payment_timestamp")))

# -------------------------
# Aggregate total payments per customer for current month
# -------------------------
df_agg = df_current.groupBy("customer_id", "year", "month") \
    .agg(sum("payment_amount").alias("total_payment"))

# Use psycopg2 to delete current month records first
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)
cur = conn.cursor()

# Delete existing current month records
cur.execute("""
    DELETE FROM customer_monthly_payments
    WHERE month = %s
      AND year = %s
""", (datetime.now().month, datetime.now().year))
conn.commit()
cur.close()
conn.close()

# -----------------------------
# Write aggregated results to PostgreSQL
# -----------------------------
jdbc_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

properties = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}

# Append the latest aggregation
df_agg.write.jdbc(
    url=jdbc_url,
    table=POSTGRES_TABLE,
    mode="append",
    properties=properties
)

print("Current month payments aggregated and written to PostgreSQL successfully!")

spark.stop()