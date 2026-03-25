import numpy as np
from datetime import datetime, timedelta
import time
from ingestion.kafka.payment_producer import send_to_kafka

# Config
start = datetime(2024, 1, 1)   
end = datetime(2025, 12, 31)
num_customers = 900000


# Generate payment event template
def generate_payment_event(customer_id, timestamp, payment_id):
    return {"payment_id": payment_id,
        "customer_id": customer_id,
        "payment_amount": round(np.random.uniform(20000, 200000), 2),
        "payment_channel": np.random.choice(["debit_card", "bank_transfer", "mobile_payment"]),
        "payment_timestamp": timestamp
    }



# Simulate payment events
def simulate_payments():
    current = start
    payment_id = 1
    while current <= end:
        for i in range(1500):
            customer_id = np.random.randint(1, num_customers+1)
            timestamp = current + timedelta(hours=np.random.randint(0, 23))
            data = generate_payment_event(customer_id, timestamp.isoformat(), payment_id)
            send_to_kafka(data)

            #time.sleep(0.1)  # Simulate streaming delay
            
            # Increment payment_id for uniqueness
            payment_id += 1

        # Increment current day after processing batch of events for the day
        current += timedelta(days=1)
    

if __name__ == "__main__":
    simulate_payments()
    print(f"{num_customers} customers payment events simulated successfully!")
        