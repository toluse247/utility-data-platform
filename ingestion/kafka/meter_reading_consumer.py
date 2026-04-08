# kafka_to_s3_meter_readings.py

from kafka import KafkaConsumer
import json
import os
import boto3
import pandas as pd
from datetime import datetime
from dateutil import parser
import uuid

# -------------------------
# Config
# -------------------------
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "meter_readings"

S3_BUCKET = os.getenv("S3_BUCKET", "utility-data-bucket")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin1234")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

BATCH_SIZE = 100  # number of records per upload

# -------------------------
# S3 Client
# -------------------------
s3 = boto3.client(
    "s3",
    endpoint_url='http://minio:9000',  # MinIO API
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# -------------------------
# Kafka Consumer
# -------------------------
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='latest',
    group_id='meter_reading_s3_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(f"Consuming from {TOPIC_NAME} and writing to S3...")

# -------------------------
# Helper: Upload to S3
# -------------------------
def upload_to_s3(records):
    if not records:
        print("No records to upload")
        return

    df = pd.DataFrame(records)

    if df.empty:
        print("DataFrame is empty")
        return

    if "read_timestamp" not in df.columns:
        print("Missing read_timestamp column")
        return

    # Convert timestamp
    df["read_timestamp"] = pd.to_datetime(df["read_timestamp"])

    # Partition columns
    df["year"] = df["read_timestamp"].dt.year
    df["month"] = df["read_timestamp"].dt.month
    df["day"] = df["read_timestamp"].dt.day
    df["hour"] = df["read_timestamp"].dt.hour

    # Build S3 path (data lake partitioning)
    now = datetime.now()
    file_name = f"meter_readings_{uuid.uuid4().hex}.csv"

    s3_key = (
        f"meter_readings/"
        f"year={df['year'].iloc[0]}/"
        f"month={df['month'].iloc[0]}/"
        f"day={df['day'].iloc[0]}/"
        f"hour={df['hour'].iloc[0]}/"
        f"{file_name}"
    )

    # Save locally then upload
    local_file = f"/Users/tolu_/Documents/utility-data-platform/tmp/{file_name}"
    df.to_csv(local_file, index=False)

    s3.upload_file(local_file, S3_BUCKET, s3_key)

    print(f"Uploaded {len(df)} records to s3://{S3_BUCKET}/{s3_key}")

# -------------------------
# Consume & Batch
# -------------------------
buffer = []

for message in consumer:
    try:
        data = message.value

        # Ensure timestamp is clean
        data["read_timestamp"] = parser.isoparse(data["read_timestamp"]).isoformat()

        buffer.append(data)

        # Upload in batches
        if len(buffer) >= BATCH_SIZE:
            upload_to_s3(buffer)
            buffer = []

    except Exception as e:
        print(f"Error processing message: {e}")