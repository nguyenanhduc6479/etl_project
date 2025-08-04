from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# --- Định nghĩa DAG ---
with DAG(
    dag_id="daily_json_to_delta_etl",
    start_date=pendulum.datetime(2025, 7, 9, tz="Asia/Ho_Chi_Minh"),
    schedule="@daily",  # Chạy hằng ngày vào lúc nửa đêm
    catchup=False,
    tags=["etl", "spark", "delta_lake"],
    doc_md="""
    ### ETL Pipeline hằng ngày
    - **Nguồn:** File JSON log hằng ngày.
    - **Đích:** Delta Lake table.
    - **Mô tả:** DAG này chịu trách nhiệm điều phối Spark job để xử lý file log JSON của ngày hôm đó và ghi kết quả vào Delta Lake.
    """,
) as dag:
    # --- Định nghĩa Task ---
    submit_spark_etl_job = SparkSubmitOperator(
        task_id="submit_spark_json_to_delta_job",
        conn_id="spark_default",

        # Đường dẫn đến file JAR bên trong container Spark
        application="/opt/bitnami/spark/app/etl_project/target/scala-2.12/etl_project_2.12-0.1.0-SNAPSHOT.jar",

        # SỬA LỖI: Tham số đúng là 'java_class', không phải 'main_class'
        java_class="mainCode.mainApp",
        packages="io.delta:delta-spark_2.12:3.1.0",

        # Cấu hình cho Spark, đặc biệt là cho Delta Lake
        conf={
            "spark.master": "spark://spark-master:7077",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        },

        # Truyền tham số với đường dẫn tương đối bên trong container
        application_args=[
            "/data/log_content/20220402.json",
            "/data/log_result/20220402"
        ],
    )
