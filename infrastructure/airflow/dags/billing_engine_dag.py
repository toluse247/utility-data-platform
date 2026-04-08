from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    "billing_engine",
    start_date=datetime(2026, 3, 24),
    schedule_interval="0 12 1 * *",
    catchup=False
)

PGPASSWORD = 'admin1234'

task1 = BashOperator(
    task_id="create_staging_tables",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db \
        -f /opt/airflow/scripts/create_staging_tables.sql \
    """,
    dag=dag
)

task2 = BashOperator(
    task_id="fetch_prev_month_reading",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db \
        -f /opt/airflow/scripts/fetch_prev_month_reading.sql \
    """,
        dag=dag
    )

task3 = BashOperator(
    task_id="fetch_current_month_reading",
    bash_command = """
        python3 /opt/airflow/scripts/fetch_current_month_reading.py
    """,
        dag=dag
    )

task4 = BashOperator(
    task_id="input_manual_readings",
    bash_command = """
        python3 /opt/airflow/scripts/input_manual_readings.py
    """,
        dag=dag
    )

task5 = BashOperator(
    task_id="append_current_month_reading",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/append_current_month_reading.sql
    """,
        dag=dag
    )

task6 = BashOperator(
    task_id="populate_staging_tables",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/populate_staging_tables.sql
    """,
        dag=dag
    )

task7 = BashOperator(
    task_id="input_feeder_readings",
    bash_command = """
        python3 /opt/airflow/scripts/input_feeder_readings.py
    """,
        dag=dag
    )

task8 = BashOperator(
    task_id="calculate_estimated_bill",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/calculate_estimated_bill.sql
    """,
        dag=dag
    )

task9 = BashOperator(
    task_id="join_billing_tables",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/join_billing_tables.sql
    """,
        dag=dag
    )

task10 = BashOperator(
    task_id="insert_final_bills",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/insert_final_bills.sql
    """,
        dag=dag
    )

task11 = BashOperator(
    task_id="delete_staging_tables",
    bash_command = f"""
        PGPASSWORD={PGPASSWORD} psql -h postgres -U admin -p 5432 -d utility_db -P admin1234 \
        -f /opt/airflow/scripts/delete_staging_tables.sql
    """,
        dag=dag
    )

task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7 >> task8 >> task9 >> task10 >> task11