from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    "data_update",
    start_date=datetime(2026, 4, 8),
    schedule_interval="0 12 28 * *",
    catchup=False
)


task1 = BashOperator(
    task_id="master_data_update",
    bash_command = f"""
        python3  /opt/airflow/scripts/updates/master_data_update.py
    """,
    dag=dag
)

task2 = BashOperator(
    task_id="customer_data_update",
    bash_command = f"""
        python3  /opt/airflow/scripts/updates/customer_data_update.py
    """,
    dag=dag
)

task1 >> task2