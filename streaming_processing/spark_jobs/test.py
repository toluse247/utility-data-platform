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
    .config("spark.hadoop.fs.s3a.signing-algorithm", "S3SignerType") \
    .getOrCreate()


hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.access.key", "minioadmin")
hadoop_conf.set("fs.s3a.secret.key", "minioadmin")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")


# -----------------------------
# TEST: Read from S3
# -----------------------------

df = spark.read \
    .option("header", True) \
    .option("recursiveFileLookup", "true") \
    .csv("s3a://utility-data-bucket/meter_readings/")

print("Data read from S3:")
df.show(5)