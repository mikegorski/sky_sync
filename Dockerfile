FROM python:3.11-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements-docker.txt .
RUN pip install --no-compile --no-cache-dir --upgrade pip \
 && pip install --no-compile --no-cache-dir -r requirements-docker.txt

COPY sky_sync/ ./sky_sync
ENTRYPOINT python sky_sync/manage.py makemigrations \
 && python sky_sync/manage.py migrate \
 && python sky_sync/manage.py runserver 0.0.0.0:8000 \
 && rm -r sky_sync/sky_sync/__pycache__/
