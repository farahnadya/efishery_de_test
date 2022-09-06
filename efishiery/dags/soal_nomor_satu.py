import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from nomor_satu.dim_customer import main_customer
from nomor_satu.dim_date import main_date
from nomor_satu.fact_order import main_fact


default_args = {
    'owner': 'farah',
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id="efishiery_nomor_satu",
    default_args=default_args,
    start_date=datetime(2022, 9, 1),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = PythonOperator(
        task_id="insert_dim_customer",
        python_callable=main_customer
    )
    task2 = PythonOperator(
        task_id="insert_dim_date",
        python_callable=main_date
    )
    task3 = PythonOperator(
        task_id="insert_fact_order_accumulating",
        python_callable=main_fact
    )
    task1>>task2>>task3