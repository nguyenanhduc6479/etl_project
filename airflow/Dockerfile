# Bắt đầu từ image Airflow chính thức
FROM apache/airflow:2.9.2
 
# Chuyển sang user root để có quyền cài đặt các gói hệ thống
USER root
 
# Cài đặt Java và các tools hữu ích
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        procps \
        netcat-traditional \
        curl \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
 
# Download và cài đặt Spark (QUAN TRỌNG để có SPARK_HOME)

ARG SPARK_VERSION=3.5.1
ARG HADOOP_VERSION=3

ENV SPARK_VERSION=${SPARK_VERSION}
ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV SPARK_HOME=/opt/spark
 
# SỬA LỖI: Sử dụng link tải ổn định hơn từ archive.apache.org
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME} && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
 
# Set ownership
RUN chown -R airflow:root ${SPARK_HOME}
 
# Set all required environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_CONF_DIR=${SPARK_HOME}/conf
# SỬA LỖI: Thêm JAVA_HOME/bin vào PATH
ENV PATH=${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${JAVA_HOME}/bin
 
 
# Chuyển lại sang user airflow
USER airflow
 
# Cài đặt Python packages
# Thêm file ràng buộc để đảm bảo tính tương thích

RUN pip install --no-cache-dir \
    "apache-airflow-providers-apache-spark" \
    "pyspark==${SPARK_VERSION}" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.12.txt"

# Set Python environment for PySpark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Verify installation
USER root
RUN echo "Checking installations..." && \
    echo "SPARK_HOME: ${SPARK_HOME}" && \
    echo "JAVA_HOME: ${JAVA_HOME}" && \
    echo "PATH: ${PATH}" && \
    which spark-submit && \
    su airflow -c "spark-submit --version"
USER airflow