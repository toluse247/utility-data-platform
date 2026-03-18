import numpy as np
from datetime import datetime, timedelta
import time
from ingestion.kafka.meter_reading_producer import sendtokafka

# Config
start = datetime(2024, 1, 1)
end = datetime(2025, 12, 31)

num_customers = 100
base_reading = 1000
variation = 5  # realistic hourly increment

# Initialize customer base meter states
customer_readings = {
    customer_id: base_reading for customer_id in range(1, num_customers + 1)
}

def generate_meter_reading(customer_id, timestamp, meter_reading_id):
    return {
        "meter_reading_id": meter_reading_id,
        "customer_id": customer_id,
        "meter_number": f"MTR{customer_id:06d}",
        "read_timestamp": timestamp.isoformat(),
        "meter_reading": round(customer_readings[customer_id], 2)
    }

def simulate_meter_readings():
    meter_reading_id = 1
    current = start

    while current <= end:
        for customer_id in range(1, num_customers + 1):

            # Increment reading
            customer_readings[customer_id] += np.random.uniform(0.1, variation)

            data = generate_meter_reading(customer_id, current, meter_reading_id)

            sendtokafka(data)

            meter_reading_id += 1

        print(f"Sent batch for {current}")

        # Simulate streaming delay
        time.sleep(0.5)  # adjust for speed

        current += timedelta(hours=1)


if __name__ == "__main__":
    simulate_meter_readings()
    print(f"{num_customers} customers meter readings simulated successfully!")