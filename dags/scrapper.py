"""A DAG for web scraping pipeline."""
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from scripts.scraping_functions import task_scrape_ids_and_hrefs
# Importa otras funciones de scraping que necesites

default_args = {
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('web_scraping_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    scrape_ids_and_hrefs = PythonOperator(
        task_id='scrape_ids_and_hrefs',
        python_callable=task_scrape_ids_and_hrefs,
    )
    