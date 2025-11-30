#!/bin/bash

set -e

echo "Starting deployment script..."

echo "Starting Celery..."
python -m celery -A src.core.celery worker --loglevel=info &

echo "Starting Gunicorn..."
exec python -m gunicorn src.core.wsgi:application --bind 0.0.0.0:$PORT --workers 2