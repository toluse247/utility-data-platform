from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    "update_payments",
    start_date=datetime(2026, 3, 24),
    schedule_interval="*/5 * * * *",
    catchup=False
)

task = BashOperator(
    task_id="update_current_month_payments",
    bash_command = """
        spark-submit \
        --master spark://spark-master:7077 \
        --packages com.datastax.spark:spark-cassandra-connector_2.12:3.4.1,org.postgresql:postgresql:42.7.3 \
        /opt/airflow/scripts/update_current_month_payments.py
    """,
    dag=dag
)