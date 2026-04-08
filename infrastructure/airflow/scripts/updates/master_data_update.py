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


# Function to cast proper data types
def data_type_conversion(df, conv_dict):
    if df is None or df.empty:
        return None

    for col, dtype in conv_dict.items():
        if col in df.columns:
            try:
                if "datetime" in str(dtype):
                    df[col] = pd.to_datetime(df[col])
                else:
                    df[col] = df[col].astype(dtype)
            except Exception as e:
                logging.error(f"Error casting {col}: {e}")
                return None

    return df

# Function to perform update in PostgreSQL
def bulk_update(conn, df, table, key_col, value_col, target_col):
    if df is None or df.empty:
        return
    cursor = conn.cursor()
    data = list(zip(df[key_col], df[value_col]))
    query = f"""
        UPDATE {table} AS t
        SET {target_col} = v.value
        FROM (VALUES %s) AS v(key, value)
        WHERE t.{key_col} = v.key
    """
    execute_values(cursor, query, data)
    cursor.close()

def append_record(df, record_table_name, conn):
    if df is None or df.empty:
        return
    cursor = conn.cursor()
    
    values = list(df.itertuples(index=False, name=None))
    columns = ", ".join(df.columns)

    query = f"""
        INSERT INTO {record_table_name} ({columns})
        VALUES %s
    """

    execute_values(cursor, query, values)
    cursor.close()

    print("Records inserted successfully!")

def main():

    # Read CSV files into DataFrames
    df_band = load_csv_from_drive("1q0bLNHzl0GkOzAiyX2w8LZQNe1UR3pGH", "band_update")
    df_feeder = load_csv_from_drive("1GSCe5556veFK2HD9AdMiS5snDcMej9XE", "feeder_update")
    df_sales_rep = load_csv_from_drive("1zKMAGTEDOcK5BYX-Gf3kIqpxq-5gOlKc", "sales_rep_update")
    df_tariff = load_csv_from_drive("1TTWfTQcwzBNnFgJ1U9x_CZcjIyrM7gYX", "tariff_rate_update")
    df_transformer = load_csv_from_drive("1TQVpaHdsIJuOk7RlNFWodXOzuHdGlS9_", "transformer_update")
    df_vat = load_csv_from_drive("1SgNs4vWGJSsm0zbGNIZ5UQwAMM6XKLX9", "vat_rate_update")
    print(df_band.head())

    # Ensure proper data types for dataframes
    df_band_conv_dict = {
        "band_update_id": int,
        "feeder_id": int,
        "new_band_id": int,
        "request_date": 'datetime64[ns]'
    }

    df_feeder_conv_dict = {
        "feeder_update_id": int,
        "transformer_id": int,
        "new_feeder_id": int,
        "request_date": 'datetime64[ns]'
    }

    df_sales_rep_conv_dict = {
        "sales_rep_update_id": int,
        "transformer_id": int,
        "new_sales_rep_id": int,
        "request_date": 'datetime64[ns]'
    }

    df_tariff_conv_dict = {
        "tariff_rate_update_id": int,
        "band_id": int,
        "new_tariff_rate": float,
        "request_date": 'datetime64[ns]'
    }

    df_transformer_conv_dict = {
        "transformer_update_id": int,
        "customer_id": int,
        "new_transformer_id": int,
        "request_date": 'datetime64[ns]'
    }

    df_vat_conv_dict = {
        "vat_rate_update_id": int,
        "band_id": int,
        "new_vat_rate": float,
        "request_date": 'datetime64[ns]'
    }


#Set environment variables for PostgreSQL connection in the terminal before running the script
#export POSTGRES_USER="admin"
#export POSTGRES_PASSWORD="admin1234"
#export POSTGRES_DB="utility_db"


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
        # Apply updates to the master data table
        if df_band is not None and not df_band.empty:

            df_band = data_type_conversion(df_band, df_band_conv_dict)
            bulk_update(conn, df_band, "feeders", "feeder_id", "new_band_id", "band_id")
            append_record(df_band, "band_update_records", conn)
            
        if df_feeder is not None and not df_feeder.empty:
            df_feeder = data_type_conversion(df_feeder, df_feeder_conv_dict)
            bulk_update(conn, df_feeder, "transformers", "transformer_id", "new_feeder_id", "feeder_id")
            append_record(df_feeder, "feeder_update_records", conn)

        if df_sales_rep is not None and not df_sales_rep.empty:
            df_sales_rep = data_type_conversion(df_sales_rep, df_sales_rep_conv_dict)
            bulk_update(conn, df_sales_rep, "transformers", "transformer_id", "new_sales_rep_id", "sales_rep_id")
            append_record(df_sales_rep, "sales_rep_update_records", conn)

        if df_tariff is not None and not df_tariff.empty:
            df_tariff = data_type_conversion(df_tariff, df_tariff_conv_dict)
            bulk_update(conn, df_tariff, "band_tariff", "band_id", "new_tariff_rate", "tariff_rate")
            append_record(df_tariff, "tariff_rate_update_records", conn)

        if df_transformer is not None and not df_transformer.empty:
            df_transformer = data_type_conversion(df_transformer, df_transformer_conv_dict)
            bulk_update(conn, df_transformer, "customers", "customer_id", "new_transformer_id", "transformer_id")
            append_record(df_transformer, "transformer_update_records", conn)

        if df_vat is not None and not df_vat.empty:
            df_vat = data_type_conversion(df_vat, df_vat_conv_dict)
            bulk_update(conn, df_vat, "band_tariff", "band_id", "new_vat_rate", "vat_rate")
            append_record(df_vat, "vat_rate_update_records", conn)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        print("Master data updates applied and records appended successfully!")
        conn.close()

if __name__ == "__main__":
    main()