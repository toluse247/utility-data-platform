import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()

# -------------------------------
# Counts for each level
# -------------------------------
num_regions = 4
num_districts = 12
num_service_units = 30
num_feeders = 120
num_transformers = 4000
num_sales_reps = 200
num_bands = 5

# -------------------------------
# 1. Regions
# -------------------------------
region_data = {
    "region_id": np.arange(1, num_regions+1),
    "region_name": ["North", "South", "East", "West"]
}
df_region = pd.DataFrame(region_data)
df_region.to_csv('regions.csv', index=False)

# -------------------------------
# 2. Districts
# -------------------------------
district_data = {
    "district_id": np.arange(1, num_districts+1),
    "district_name": [fake.city() for _ in range(num_districts)],
    "region_id": np.random.choice(df_region['region_id'], num_districts)
}
df_districts = pd.DataFrame(district_data)
df_districts.to_csv('districts.csv', index=False)

# -------------------------------
# 3. Service Units
# -------------------------------
service_unit_data = {
    "service_unit_id": np.arange(1, num_service_units+1),
    "service_unit_name": [f"Service_Unit_{i}" for i in range(1, num_service_units+1)],
    "district_id": np.random.choice(df_districts['district_id'], num_service_units)
}
df_service_units = pd.DataFrame(service_unit_data)
df_service_units.to_csv('service_units.csv', index=False)

# -------------------------------
# 4. Feeders
# -------------------------------
band_ids = np.arange(1, num_bands+1)
feeder_data = {
    "feeder_id": np.arange(1, num_feeders+1),
    "feeder_name": [f"Feeder_{i}" for i in range(1, num_feeders+1)],
    "band_id": np.random.choice(band_ids, num_feeders),
    "service_unit_id": np.random.choice(df_service_units['service_unit_id'], num_feeders)
}
df_feeder = pd.DataFrame(feeder_data)
df_feeder.to_csv('feeders.csv', index=False)

# -------------------------------
# 5. Bands
# -------------------------------
bands_data = {
    "band_id": np.arange(1, num_bands+1),
    "band_name": ["A", "B", "C", "D", "E"],
    "tariff_rate": [200.75,150.50, 100.25, 75.00, 50.00],
    "vat_rate": [0.075, 0.075, 0.075, 0.075, 0.075]
}
df_bands = pd.DataFrame(bands_data)
df_bands.to_csv('bands.csv', index=False)

# -------------------------------
# 5. Transformers
# -------------------------------
transformer_data = {
    "transformer_id": np.arange(1, num_transformers+1),
    "transformer_name": [f"Transformer_{i}" for i in range(1, num_transformers+1)],
    "sales_rep_id": np.random.randint(1, num_sales_reps+1, num_transformers),
    "feeder_id": np.random.choice(df_feeder['feeder_id'], num_transformers)
}
df_transformer = pd.DataFrame(transformer_data)
df_transformer.to_csv('transformers.csv', index=False)

# -------------------------------
# 6. Sales Reps
# -------------------------------
sales_rep_data = {
    "sales_rep_id": np.arange(1, num_sales_reps+1),
    "sales_rep_name": [fake.name() for _ in range(num_sales_reps)],
    "sales_rep_phone": [fake.phone_number() for _ in range(num_sales_reps)]
}
df_sales_rep = pd.DataFrame(sales_rep_data)
df_sales_rep.to_csv('sales_reps.csv', index=False)

print("Hierarchy data generated successfully!")