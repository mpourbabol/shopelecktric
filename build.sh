#!/usr/bin/env bash
set -o errexit

if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set."
  echo "In Render: create PostgreSQL, then add its Internal Database URL as DATABASE_URL."
  exit 1
fi

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_home_appliances
python manage.py ensure_deploy_admin
