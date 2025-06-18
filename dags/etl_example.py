from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import pandas as pd
import os

dag_path = os.path.dirname(__file__)


def extract():
    dag_path = os.path.dirname(__file__)
    csv_path = os.path.join(dag_path, 'transaction_data.csv')

    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['TransactionTime'].str.replace('IST', ''), errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    df.to_csv('/tmp/extracted_data.csv', index=False)
    
def transform():
    df = pd.read_csv('/tmp/extracted_data.csv')
    result = df.groupby(['Country','Year','Month'])['NumberOfItemsPurchased'].sum().reset_index()
    result.to_csv('/tmp/transformed_data.csv', index=False)

def load():
    df = pd.read_csv('/tmp/transformed_data.csv')
    csv_path = os.path.join(dag_path, 'OLAP_data.csv')
    df.to_csv(csv_path, index=False)

with DAG(
    dag_id='etl_example',
    start_date=datetime(2023, 1, 1),
    # schedule_interval='@daily',
    schedule='@daily',
    catchup=False,
    tags=['example', 'etl']
) as dag:
    
    t1 = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    t2 = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    t3 = PythonOperator(
        task_id='load',
        python_callable=load
    )

    #task order
    t1 >> t2 >> t3
