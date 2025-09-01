#!/usr/bin/env python3
import os
import sys
import shlex
import subprocess

from superset.app import create_app

def run(cmd: str) -> None:
    print("+", cmd, flush=True)
    subprocess.run(shlex.split(cmd), check=True)

def main() -> None:
    print("== Superset init (Python) ==")

    # --- envs (must be set in docker-compose) ---
    admin_user  = os.environ.get("ADMIN_USERNAME")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_pass  = os.environ.get("ADMIN_PASSWORD")

    missing = [k for k,v in {
        "ADMIN_USERNAME": admin_user,
        "ADMIN_EMAIL": admin_email,
        "ADMIN_PASSWORD": admin_pass,
    }.items() if not v]
    if missing:
        print(f"ERROR: missing envs: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # 1) Migrate metadata DB
    run("superset db upgrade")

    # 2) Create/reset admin in app context
    app = create_app()
    with app.app_context():
        from superset import security_manager, db

        user = security_manager.find_user(username=admin_user)
        if user:
            print(f"Admin '{admin_user}' already exists -> resetting password")
            # Prefer CLI for compatibility; fall back to API if needed
            try:
                run(f"superset fab reset-password --username {admin_user} --password {admin_pass}")
            except subprocess.CalledProcessError:
                # Fallback (older/newer APIs): hash & set
                try:
                    user.password = security_manager.hash_password(admin_pass)
                    db.session.commit()
                except Exception as e:
                    print(f"ERROR resetting password: {e}", file=sys.stderr)
                    sys.exit(1)
        else:
            print(f"Creating admin '{admin_user}'")
            role_admin = security_manager.find_role("Admin")
            # Some versions take roles=[...], others role=...
            try:
                new_user = security_manager.add_user(
                    username=admin_user,
                    first_name="Admin",
                    last_name="User",
                    email=admin_email,
                    roles=[role_admin],
                    password=admin_pass,
                )
            except TypeError:
                new_user = security_manager.add_user(
                    username=admin_user,
                    first_name="Admin",
                    last_name="User",
                    email=admin_email,
                    role=role_admin,
                    password=admin_pass,
                )
            if not new_user:
                print("ERROR: could not create admin user", file=sys.stderr)
                sys.exit(1)
            db.session.commit()

    # 3) Seed roles/perm & finalize
    run("superset init")
    print("== Superset init DONE ==")

if __name__ == "__main__":
    main()
