#!/usr/bin/env bash
set -euo pipefail

# 1) Migrate metadata DB
airflow db migrate

# 2) Tạo/đảm bảo admin từ .env (bắt buộc)
: "${AIRFLOW_ADMIN_USER:?Missing AIRFLOW_ADMIN_USER}"
: "${AIRFLOW_ADMIN_PASSWORD:?Missing AIRFLOW_ADMIN_PASSWORD}"
airflow users create --username "$AIRFLOW_ADMIN_USER" --password "$AIRFLOW_ADMIN_PASSWORD" --firstname "Admin" --lastname "User" --role "Admin" --email "admin@example.org" || true
echo "admin ensured"

# 3) (Tuỳ chọn) tạo user thường nếu có đủ biến trong .env
if [[ -n "${AIRFLOW_USER_USERNAME:-}" && -n "${AIRFLOW_USER_PASSWORD:-}" ]]; then
  airflow users create --username "$AIRFLOW_USER_USERNAME" --password "$AIRFLOW_USER_PASSWORD" --firstname "Normal" --lastname "User" --role "User" --email "user@example.org" || true
  echo "normal user ensured"
fi

# 4) Tạo connection spark_default trong DB (tránh env override)
SPARK_MASTER_URL="${SPARK_MASTER_URL:-spark://spark-master:7077}"
while airflow connections delete spark_default >/dev/null 2>&1; do :; done || true
airflow connections add spark_default --conn-type spark --conn-host "spark://spark-master:7077"
airflow connections get spark_default
echo "Init done."