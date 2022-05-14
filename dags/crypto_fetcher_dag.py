  
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflowag.models import Variable
from datetime import datetime

default_args = {
    "owner": "airflow",
    "provide_context": True,
    "email_on_failure": False,
}

coins = Variable.get("files_list", deserialize_json=True)

with DAG(
    "crypto_fetcher_dag",
    start_date=datetime(2022, 4, 23),
    default_args=default_args,
    schedule_interval="0 3 * * *",
    catchup=False,
    params={"start_date": "2022-04-01", "end_date": "2022-04-24"}
) as dag:


    start = DummyOperator(task_id="start")


    coins_tasks = list()
    start_date = '{{ dag_run.conf["start_date"] }}'
    end_date = '{{ dag_run.conf["end_date"] }}'
    for coin in coins:
        task  = BashOperator(
            task_id=f"fetch_{coin}",
            bash_command=f'crypto_fetcher.py -c {coin} -s {start_date} -e {end_date} --save-db',
        )
        coins_tasks.append(task)

    end = DummyOperator(task_id="end")

    start >> [coins_tasks] >> end