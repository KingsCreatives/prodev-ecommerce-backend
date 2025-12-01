#!/bin/bash
set -e

echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Applying database migrations..."
python src/manage.py migrate

echo "Checking for superuser..."
python -c "
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if password:
    if not User.objects.filter(email=email).exists():
        print(f'Creating superuser {username} ({email})...')
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created successfully.')
    else:
        print('Superuser already exists. Skipping.')
else:
    print('No DJANGO_SUPERUSER_PASSWORD set. Skipping superuser creation.')
"

echo "Starting deployment script..."

echo "Starting Celery..."
python -m celery -A src.core worker --loglevel=info &

echo "Starting Gunicorn..."
exec python -m gunicorn src.core.wsgi:application --bind 0.0.0.0:$PORT --workers 2