from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, year, month
from pyspark.sql.types import TimestampType

# -------------------------
# Initialize Spark
# -------------------------
spark = SparkSession.builder \
    .appName("MonthlyPaymentsAggregation") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .getOrCreate()

# -------------------------
# Read from Cassandra
# -------------------------
df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="payments", keyspace="utility_db") \
    .load()

# -------------------------
# Ensure timestamp is proper type
# -------------------------
df = df.withColumn(
    "payment_timestamp",
    col("payment_timestamp").cast(TimestampType())
)

# -------------------------
# Extract year & month
# -------------------------
df = df.withColumn("year", year(col("payment_timestamp"))) \
       .withColumn("month", month(col("payment_timestamp")))

# -------------------------
# Aggregate
# -------------------------
agg_df = df.groupBy("customer_id", "year", "month") \
    .agg(sum("payment_amount").alias("total_payment"))

# -------------------------
# Write to PostgreSQL
# -------------------------
agg_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/utility_db") \
    .option("dbtable", "customer_monthly_payments") \
    .option("user", "admin") \
    .option("password", "admin1234") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print("Aggregation completed and written to PostgreSQL.")