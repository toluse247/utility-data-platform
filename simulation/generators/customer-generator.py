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
num_customers = 1000000
num_transformers = 4000
start = datetime(2024, 1, 1)
end = datetime(2025, 12, 31)

# Pre-generate pools (speed optimization)
name_pool = [fake.name() for _ in range(10000)]
address_pool = [fake.address().replace("\n", ", ") for _ in range(10000)]
email_pool = [fake.email() for _ in range(10000)]
phone_pool = [fake.phone_number() for _ in range(10000)]

# Generate customer data in chunks
size = 100000
for i in range(num_customers // size):
    start_idx = i * size + 1
    end_idx = (i + 1) * size + 1

    customer_data = {
        "customer_id": np.arange(start_idx, end_idx),
        "meter_number": [f"MTR{i:06d}" for i in range(start_idx, end_idx)],
        "customer_name": np.random.choice(name_pool, size),
        "address": np.random.choice(address_pool, size),
        "customer_phone": np.random.choice(phone_pool, size),
        "customer_type": np.random.choice(["Residential", "Commercial", "Industrial"], size),
        "billing_type": np.random.choice(["R","D"], size),
        "transformer_id": np.random.randint(1, num_transformers+1, size),
        "account_status": np.random.choice(["ACTIVE", "INACTIVE"], size),
        "latitude": np.around(np.random.uniform(5, 7, size), 6),
        "longitude": np.around(np.random.uniform(5, 7, size), 6),
        "email": np.random.choice(email_pool, size),
        "created_at": random_timestamp(start, end, size),
    }

    # Create DataFrame
    df = pd.DataFrame(customer_data)

    # Export and append to file
    df.to_csv('customers.csv', index=False, mode='a', header=(i==0))
    print(f"{start_idx} to {end_idx-1} customers records generated successfully!")

print(f"{num_customers} customers records generated successfully!")



