import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to load CSV from Google Drive
def load_csv_from_drive(file_id, name):
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_csv(url)
        print(f"✅ {name} loaded successfully")
        return df

    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
        return None    

#-----------------------------------------------
# Function to perform name update in PostgreSQL
#-----------------------------------------------
def bulk_update(conn, df, table, key_col, value_col, target_col):
    if df is None or df.empty:
        return
    cursor = conn.cursor()
    data = list(zip(df[key_col], df[value_col]))
    if target_col == "billing_type":
        df = df[df["new_billing_type"].str.upper().isin(["R", "D"])]
        df["new_billing_type"] = df["new_billing_type"].str.upper()
    if target_col == "account_status":
        df = df[df["new_status"].str.upper().isin(["ACTIVE", "INACTIVE"])]
        df["new_status"] = df["new_status"].str.upper()

    query = f"""
        UPDATE {table} AS t
        SET {target_col} = v.value
        FROM (VALUES %s) AS v(key, value)
        WHERE t.{key_col} = v.key
    """

    execute_values(cursor, query, data)
    cursor.close()
    logging.info("Customer data updated successfully!")

def main():
    # Read CSV files into DataFrames
    df_name = load_csv_from_drive("1UD0M9oc5DT6LrHypWHhvbTM5kRFXwhZH", "name_update")
    df_address = load_csv_from_drive("1wNp2FISwng5BhRkmhi4o6rBqJTOH7VBi", "address_update")
    df_status = load_csv_from_drive("1BzsuvQJPqz2VJTfZEFS7_3xUEhCJhq23", "status_update")
    df_billing_type = load_csv_from_drive("1hgKIkVNLzt90tA1CUFOc20YVFIZFShwH", "billing_type_update")

    #--------------------------
    # Ensure proper data types
    #--------------------------
    if df_name is not None and not df_name.empty:
        df_name["customer_id"] = df_name["customer_id"].astype(int)
        df_name["new_name"] = df_name["new_name"].astype(str)
    if df_address is not None and not df_address.empty:
        df_address["customer_id"] = df_address["customer_id"].astype(int)
        df_address["new_address"] = df_address["new_address"].astype(str)
    if df_status is not None and not df_status.empty:
        df_status["customer_id"] = df_status["customer_id"].astype(int)
        df_status["new_status"] = df_status["new_status"].astype(str)
    if df_billing_type is not None and not df_billing_type.empty:
        df_billing_type["customer_id"] = df_billing_type["customer_id"].astype(int)
        df_billing_type["new_billing_type"] = df_billing_type["new_billing_type"].astype(str)



    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    conn = psycopg2.connect(
        host="postgres",
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=5432
    )

    logging.info("Connected to PostgreSQL successfully!")
    try:

        if df_name is not None and not df_name.empty:
            bulk_update(conn, df_name, "customers", "customer_id", "new_name", "customer_name")
        if df_address is not None and not df_address.empty:
            bulk_update(conn, df_address, "customers", "customer_id", "new_address", "address")
        if df_status is not None and not df_status.empty:
            bulk_update(conn, df_status, "customers", "customer_id", "new_status", "account_status")
        if df_billing_type is not None and not df_billing_type.empty:
            bulk_update(conn, df_billing_type, "customers", "customer_id", "new_billing_type", "billing_type")
        conn.commit()

    except Exception as e:
            conn.rollback()
            logging.error("Error occurred while updating customer data: %s", e)
    finally:
        logging.info("Master data updates applied and records appended successfully!")
        conn.close()

if __name__ == "__main__":
    main()