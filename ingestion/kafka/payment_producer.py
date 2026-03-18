from kafka import KafkaProducer
import json

# Kafka Config
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "payments"

# Initialize producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_to_kafka(data):
    try:
        producer.send(TOPIC_NAME, value=data)
        print("message has reached kafka producer")
        producer.flush()
    except Exception as e:
        print(f"Error sending to Kafka: {e}")