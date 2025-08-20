from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG("spark_connectivity_check", start_date=datetime(2024,1,1), schedule=None, catchup=False):
    SparkSubmitOperator(
        task_id="spark_pi",
        conn_id="spark_default",           # dùng master từ connection
        application="/opt/airflow/dags/apps/spark_pi.py",
        deploy_mode="client",
        total_executor_cores=1,
        executor_cores=1,
        executor_memory="512m",
        driver_memory="512m",
        verbose=True,
        # Nếu spark-submit không nằm trong PATH của container Airflow, chỉ định rõ:
        # spark_binary="/opt/bitnami/spark/bin/spark-submit",
    )