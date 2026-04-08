import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Download CSV to DataFrame
url = "https://drive.google.com/uc?export=download&id=1ubxuKJkEZUBqzTKL8xwNu-0A4iaol2qH"
df = pd.read_csv(url)

# Convert types
df["feeder_cons_id"] = df["feeder_cons_id"].astype(int)
df["feeder_id"] = df["feeder_id"].astype(int)
df["feeder_name"] = df["feeder_name"].astype(str)
df["consumption_month"] = pd.to_datetime(df["consumption_month"]).dt.date
df["consumption_kwh"] = df["consumption_kwh"].astype(float)

# Upsert function
def insert_df(df, table_name, conn):
    cursor = conn.cursor()
    values = [tuple(x) for x in df.to_numpy()]

    query = f"""
        INSERT INTO {table_name} (feeder_cons_id, feeder_id, feeder_name, consumption_month, consumption_kwh)
        VALUES %s
        ON CONFLICT (feeder_cons_id, consumption_month)
        DO UPDATE SET
            feeder_id = EXCLUDED.feeder_id,
            feeder_name = EXCLUDED.feeder_name,
            consumption_kwh = EXCLUDED.consumption_kwh
    """

    execute_values(cursor, query, values)
    conn.commit()
    cursor.close()

# Connect and insert
conn = psycopg2.connect(
    host="postgres",
    database="utility_db",
    user="admin",
    password="admin1234",
    port=5432
)

insert_df(df, "feeder_energy_consumption", conn)
conn.close()