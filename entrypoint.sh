#!/bin/sh
set -e

mkdir -p /app/data

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec gunicorn Ecosistema_Personal.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 2 \
    --access-logfile - \
    --error-logfile -
