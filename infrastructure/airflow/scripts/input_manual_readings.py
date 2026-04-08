import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Download CSV to DataFrame
url = "https://drive.google.com/uc?export=download&id=11OZdQYtC-Zu5mAcT4esSyc7boP89EClK"
df = pd.read_csv(url)

# Ensure proper data types
df["customer_id"] = df["customer_id"].astype(int)
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["meter_reading"] = df["meter_reading"].astype(float)


def upsert_df(df, table_name, conn):
    cursor = conn.cursor()

    values = [tuple(x) for x in df.to_numpy()]

    query = f"""
        INSERT INTO {table_name} (customer_id, year, month, meter_reading)
        VALUES %s
        ON CONFLICT (customer_id, year, month)
        DO UPDATE SET
            meter_reading = EXCLUDED.meter_reading
    """

    execute_values(cursor, query, values)

    conn.commit()
    cursor.close()


table_name = "stg_present_readings"
conn = psycopg2.connect(
    host="postgres",
    database="utility_db",
    user="admin",
    password="admin1234",
    port=5432
)

upsert_df(df, table_name, conn)
conn.close()