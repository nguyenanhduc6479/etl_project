from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator
from datetime import timedelta

# Default arguments
default_args = {
    'owner' : 'data-team',
    'depends_on_past' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5),
}

# --- Định nghĩa DAG ---
with DAG(
    dag_id="daily_json_to_delta_etl",
    default_args = default_args,
    start_date = pendulum.datetime(2025, 7, 9, tz="Asia/Ho_Chi_Minh"),
    schedule = None,#"@daily",  # Chạy hằng ngày vào lúc nửa đêm
    catchup = False,
    tags = ["etl", "spark", "delta_lake"],
    doc_md = """
    ### ETL Pipeline hằng ngày
    - **Nguồn:** File JSON log hằng ngày.
    - **Đích:** Delta Lake table.
    - **Mô tả:** DAG này chịu trách nhiệm điều phối Spark job để xử lý file log JSON của ngày hôm đó và ghi kết quả vào Delta Lake.
    """,
) as dag:
    
    # Task 1: Kiểm tra file JSON tồn tại
    check_source_file = BashOperator(
        task_id = "check_source_file_exists",
        bash_command = """
        FILE_PATH = "/data/log_content/20220402.json"
        if [ -f "$FILE_PATH" ]; then
            echo "Source file exists: $FILE_PATH"
            ls -la "$FILE_PATH"
        else
            echo "ERROR : Source file not found: $FILE_PATH"
            exit 1
        fi
        """,
    )
    
    # --- Định nghĩa Task ---
    submit_spark_etl_job = SparkSubmitOperator(
        task_id = "submit_spark_json_to_delta_job",
        conn_id = "spark_default",
        # Đường dẫn đến file JAR bên trong container Spark
        application = "/opt/bitnami/spark/app/etl_project/target/scala-2.12/etl_project_2.12-0.1.0-SNAPSHOT.jar",

        # Main class
        java_class = "mainCode.mainApp",
        
        # Delta lake package
        packages = "io.delta:delta-spark_2.12:3.1.0",
        
        # Cấu hình cho Spark, đặc biệt là cho Delta Lake
        conf = {
            "spark.sql.extensions" : "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog" : "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.sql.adaptive.enabled" : "true",
            "spark.sql.adaptive.coalescePartitions.enabled" : "true",
            "spark.eventLog.enabled" : "true",
            "spark.eventLog.dir" : "file:///opt/bitnami/spark/eventlogs",
        },

        # Truyền tham số với đường dẫn tương đối bên trong container
        application_args=[
            "/data/log_content/20220402.json",
            "/data/log_result/20220402"
        ],
        
        # Tài nguyên chạy job
        driver_memory = "1g",
        executor_memory = "2g",
        num_executors = 1,
        
        # Timeout
        execution_timeout = timedelta(minutes=2)
        
    )
    
    # Task 3: Validate Delta Lake output
    validate_output = BashOperator(
        task_id = "validate_delta_output",
        bash_command = """
        OUTPUT_PATH="/data/log_result/20220402"
        echo "Checking Delta Lake output at : $OUTPUT_PATH"
        
        # Check if Delta directory exists
        if [ -d "$OUTPUT_PATH" ]; then
            echo "Delta table created successfully"
            echo "Delta files:"
            find "$OUTPUT_PATH" -type f -name "*.parquet" | head -10
            echo "Total parquet files: $(find "$OUTPUT_PATH" -type f -name "*.parquet" | wc -l)"
        else
            echo "ERROR : Delta table not found at $OUTPUT_PATH"
            exit 1
        fi
        """,
    )
    
    # Set dependencies
    check_source_file >> submit_spark_etl_job >> validate_output
