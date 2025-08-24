#!/usr/bin/env bash
set -euo pipefail

echo "== Superset init =="

# Hiển thị DB URI mà Superset sẽ dùng (để kiểm tra nhanh)
python - <<'PY'
from superset.app import create_app
app = create_app()
with app.app_context():
    from flask import current_app
    print("DB URI =", current_app.config.get("SQLALCHEMY_DATABASE_URI"))
PY

# Nâng cấp schema metadata (idempotent)
superset db upgrade

: "${ADMIN_USERNAME:?Missing ADMIN_USERNAME}"
: "${ADMIN_EMAIL:?Missing ADMIN_EMAIL}"
: "${ADMIN_PASSWORD:?Missing ADMIN_PASSWORD}"

# Kiểm tra sự tồn tại của user qua app context thuần Python (chỉ in 1/0)
HAS_USER=$(python - <<'PY'
from superset.app import create_app
app = create_app()
with app.app_context():
    from superset import db
    from flask_appbuilder.security.sqla.models import User
    import os
    uname = os.environ.get("ADMIN_USERNAME")
    print("1" if db.session.query(User).filter(User.username==uname).first() else "0")
PY
)
HAS_USER="$(echo "$HAS_USER" | tr -d '\r\n[:space:]')"

if [[ "$HAS_USER" == "1" ]]; then
  echo "Admin '$ADMIN_USERNAME' đã tồn tại -> reset password"
  superset fab reset-password --username "$ADMIN_USERNAME" --password "$ADMIN_PASSWORD"
else
  echo "Tạo admin '$ADMIN_USERNAME'"
  superset fab create-admin \
    --username "$ADMIN_USERNAME" \
    --firstname Admin \
    --lastname User \
    --email "$ADMIN_EMAIL" \
    --password "$ADMIN_PASSWORD"
fi

# Khởi tạo roles/perms (idempotent)
superset init

echo "== Superset init DONE =="
