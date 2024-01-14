FROM python:3.11-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements-docker.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements-docker.txt

COPY .env .
COPY sky_sync/ ./sky_sync
CMD ["python", "sky_sync/manage.py", "runserver", "0.0.0.0:8000"]
