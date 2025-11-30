FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH=/app/src 

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --user -r /app/requirements.txt

COPY scripts /app/scripts

RUN chmod +x /app/scripts/start_render.sh

COPY src /app/src

RUN mkdir -p /app/static

CMD ["gunicorn", "src.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]