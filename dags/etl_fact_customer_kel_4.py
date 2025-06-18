from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import pandas as pd
import os

dag_path = os.path.dirname(__file__)


def extract():
    dag_path = os.path.dirname(__file__)
    csv_path = os.path.join(dag_path, 'adidas_us_sales.csv')

    df = pd.read_csv(csv_path)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Date'] = df['InvoiceDate'].dt.day
    df['Month'] = df['InvoiceDate'].dt.month
    df['Year'] = df['InvoiceDate'].dt.year

    df['PricePerUnit'] = df['PricePerUnit'].str.replace('$', '', regex=False).str.replace(',', '.', regex=False).str.strip()
    df['TotalSales'] = df['TotalSales'].str.replace('$', '', regex=False).str.replace(',', '.', regex=False).str.strip()
    df['OperatingProfit'] = df['OperatingProfit'].str.replace('$', '', regex=False).str.replace(',', '.', regex=False).str.strip()

    df['PricePerUnit'] = df['PricePerUnit'].astype(float)
    df['TotalSales'] = df['TotalSales'].astype(float)
    df['OperatingProfit'] = df['OperatingProfit'].astype(float)

    df.to_csv('/tmp/extracted_data_adidas.csv', index=False)
    
def transform():

    df = pd.read_csv('/tmp/extracted_data_adidas.csv')
    df = df.rename(columns={'TotalSales': 'Revenue'})
    result = df.groupby(['Year','Month','State','City','Product'])[['UnitsSold','Revenue','OperatingProfit']].sum().reset_index()

    result.to_csv('/tmp/transformed_data_adidas.csv', index=False)

def load():
    df = pd.read_csv('/tmp/transformed_data_adidas.csv')
    csv_path = os.path.join(dag_path, 'OLAP_data_fact_customersales.csv')
    
    df.to_csv(csv_path, index=False)

with DAG(
    dag_id='etl_fact_customer_kel_4',
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