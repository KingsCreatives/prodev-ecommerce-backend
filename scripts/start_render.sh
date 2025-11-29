#!/bin/bash
celery -A src.core.celery worker --loglevel=info &

python -m gunicorn src.core.wsgi:application --bind 0.0.0.0:$PORT --workers 2