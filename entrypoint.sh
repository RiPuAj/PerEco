#!/bin/sh
set -e

mkdir -p /app/data

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superusuario admin creado.')
else:
    print('Superusuario admin ya existe.')
"

exec gunicorn Ecosistema_Personal.wsgi:application \
    --bind 0.0.0.0:8888 \
    --workers 2 \
    --threads 2 \
    --access-logfile - \
    --error-logfile -
