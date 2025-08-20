# -------- Stage 1: Lấy Spark từ Bitnami (ổn định, không cần curl) --------
FROM bitnami/spark:3.5.1 AS sparkdist

# -------- Stage 2: Ảnh Airflow có sẵn Spark CLI --------
FROM apache/airflow:2.9.2-python3.12

# OS + JRE cho Spark
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless procps ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy Spark từ stage 1
COPY --from=sparkdist /opt/bitnami/spark /opt/spark
ENV SPARK_HOME=/opt/spark

# *** PATH CHUẨN CHO ENTRYPOINT (root) VÀ USER airflow ***
# Bổ sung rõ ràng /usr/local/bin và /home/airflow/.local/bin để 'airflow' luôn được tìm thấy
ENV PATH="/opt/spark/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/airflow/.local/bin"
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Quyền
RUN mkdir -p /opt/airflow/scripts && chown -R airflow:root /opt/spark /opt/airflow

# ---- Python deps dưới user airflow + dùng constraints để pin version provider ----
USER airflow
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.12
ENV PIP_CONSTRAINT="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

COPY --chown=airflow:root requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt --constraint "${PIP_CONSTRAINT}"

# Init script
COPY --chown=airflow:root scripts/init.sh /opt/airflow/scripts/init.sh
RUN sed -i 's/\r$//' /opt/airflow/scripts/init.sh && chmod +x /opt/airflow/scripts/init.sh

USER airflow