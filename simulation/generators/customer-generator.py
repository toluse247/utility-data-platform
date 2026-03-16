import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker() 

# Random timestamp generator
def random_timestamp(start, end, n):
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())
    random_ts = np.random.randint(start_ts, end_ts, n)
    return pd.to_datetime(random_ts, unit='s')

# Define the number of customers to generate
num_customers = 100000
num_transformers = 4000
start = datetime(2024, 1, 1)
end = datetime(2025, 12, 31)

# Generate customer data
customer_data = {
    "customer_id": np.arange(num_customers),
    "meter_number": [f"MTR{i}" for i in range(num_customers)],
    "customer_name": [fake.name() for _ in range(num_customers)],
    "address": [fake.address() for _ in range(num_customers)],
    "customer_phone": [fake.phone_number() for _ in range(num_customers)],
    "customer_type": np.random.choice(["R","D"], num_customers),
    "transformer_id": np.random.randint(1, num_transformers+1, num_customers),
    "account_status": np.random.choice(["ACTIVE", "INACTIVE"], num_customers),
    "latitude": round(np.random.uniform(5, 7, num_customers), 6),
    "longitude": round(np.random.uniform(5, 7, num_customers), 6),
    "email": [fake.email() for _ in range(num_customers)],
    "created_at": random_timestamp(start, end, num_customers)
}

# Create DataFrame
df = pd.DataFrame(customer_data)

# Export file
df.to_csv('customers_1.csv', index=False)
print("1 million customer records generated successfully!")



