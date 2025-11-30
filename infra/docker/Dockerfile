FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/src"
ENV PATH="/app/scripts:${PATH}"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev gcc dos2unix \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY scripts /app/scripts
RUN dos2unix /app/scripts/start_render.sh
RUN chmod +x /app/scripts/start_render.sh

COPY src /app/src

RUN mkdir -p /app/static

CMD ["gunicorn", "src.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]