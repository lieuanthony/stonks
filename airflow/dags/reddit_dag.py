import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators import PythonOperator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.reddit_pipeline import reddit_pipeline
from trader.trader import trade

default_args = {
    'owner': 'Anthony Lieu',
    'start_date': datetime(2025, 5, 8)
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='reddit_etl_pipeline',
    default_args=default_args,
    schedule_interval='25 14 * * *',        # Runs once per day at 9:25 AM EST
    catchup=False,                          # When set to False, it prevents Airflow from running backfilling tasks for past dates.
    tags=['reddit', 'etl', 'pipeline']      # Tags to categorize and filter the DAG.
)

# DAG 1: Extraction from reddit
extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'wallstreetbets',
        'time_filter': 'day',
        'limit': 5000
    },
    dag=dag
)

# DAG 2: Analyze output and trade stocks
analyze_and_trade = PythonOperator(
    task_id = 'analyze_and_trade',
    python_callable = trade,
    dag = dag
)

extract >> analyze_and_trade