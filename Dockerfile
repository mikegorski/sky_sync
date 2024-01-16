FROM python:3.11-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements-docker.txt .
RUN pip install --no-compile --no-cache-dir --upgrade pip \
 && pip install --no-compile --no-cache-dir -r requirements-docker.txt

COPY sky_sync/ ./sky_sync
CMD ["python", "sky_sync/manage.py", "runserver", "0.0.0.0:8000"]
