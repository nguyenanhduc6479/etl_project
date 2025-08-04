# Bắt đầu từ image Airflow chính thức
FROM apache/airflow:2.9.2

# Chuyển sang user root để có quyền cài đặt các gói hệ thống
USER root

# Cài đặt Java Runtime Environment (JRE) - cần thiết để chạy spark-submit
# SỬA LỖI: Dùng 'default-jre-headless' để tương thích với nhiều phiên bản HĐH
RUN apt-get update && \
    apt-get install -y default-jre-headless && \
    apt-get clean && \ 
    rm -rf /var/lib/apt/lists/*

# Chuyển lại sang user airflow để thực hiện các thao tác của Airflow
USER airflow

# Cài đặt gói provider cho Apache Spark, sử dụng file ràng buộc để đảm bảo tương thích
RUN pip install --no-cache-dir \
    "apache-airflow-providers-apache-spark" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.12.txt"
