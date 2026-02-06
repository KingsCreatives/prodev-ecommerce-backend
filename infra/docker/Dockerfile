FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/src"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev gcc dos2unix \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

RUN mkdir -p /app/staticfiles

RUN DJANGO_SECRET_KEY=build-only-key \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS=localhost \
    DATABASE_URL=postgres://dummy \
    python src/manage.py collectstatic --noinput

CMD ["gunicorn", "src.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]