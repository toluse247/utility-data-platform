from datetime import datetime
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import json
import os

# -------------------------
# Configurations
# -------------------------
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "payments"
CASSANDRA_HOST = "localhost"
CASSANDRA_PORT = 9042
KEYSPACE = "utility_db"
TABLE = "payments"

# -------------------------
# Initialize Cassandra
# -------------------------
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect(KEYSPACE)

insert_stmt = session.prepare(f"""
    INSERT INTO {TABLE} (
        payment_id, customer_id, payment_amount, payment_channel, payment_timestamp
    ) VALUES (?, ?, ?, ?, ?)
""")

# -------------------------
# Initialize Kafka Consumer
# -------------------------
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',  # read from beginning if no offsets
    group_id='payment_consumer_group_v4',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print(f"Listening to Kafka topic '{TOPIC_NAME}' and writing to Cassandra table '{TABLE}'...")

# -------------------------
# Consume messages
# -------------------------
for message in consumer:
    try:
        data = message.value
        session.execute(
            insert_stmt,
            (
                int(data["payment_id"]),
                int(data["customer_id"]),
                round(data["payment_amount"], 2),
                data["payment_channel"],
                datetime.fromisoformat(data["payment_timestamp"])  # must match Cassandra column type (timestamp)
            )
        )
    except Exception as e:
        print(f"Error inserting message: {e}")
    print("Inserted 1 payment event into Cassandra.")
