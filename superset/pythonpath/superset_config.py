# superset/pythonpath/superset_config.py
import os
from urllib.parse import quote_plus

DB_USER = os.environ.get("SUPERSET_USER_USERNAME")
DB_PASS = quote_plus(os.environ.get("SUPERSET_USER_PASSWORD"))
DB_HOST = os.environ.get("SUPERSET_DB_HOST")
DB_NAME = os.environ.get("SUPERSET_DB")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "PLEASE_CHANGE_ME")

# Không load sample
LOAD_EXAMPLES = False

# Giảm warning không cần thiết
SQLALCHEMY_TRACK_MODIFICATIONS = False
RATELIMIT_STORAGE_URI = "memory://"
