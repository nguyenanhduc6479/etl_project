# Bắt đầu từ image Airflow chính thức
FROM apache/airflow:2.9.2

# Chuyển sang user root để có quyền cài đặt các gói hệ thống
USER root

# Cài đặt Java và các tools hữu ích
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        # Tools để debug
        procps \
        netcat-traditional \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME (một số Spark jobs cần)
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

# Chuyển lại sang user airflow
USER airflow

# Cài đặt Python packages
# LƯU Ý: PySpark version phải match với Spark cluster version
RUN pip install --no-cache-dir "apache-airflow-providers-apache-spark" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.12.txt"

RUN pip install --no-cache-dir "pyspark==3.5.1"

# Optional: Set Spark environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3