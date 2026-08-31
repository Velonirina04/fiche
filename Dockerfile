# Use a slim Python base image
FROM python:3.11-slim

# Avoid Python writing .pyc files and enable buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for Pillow and other packages (if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY fiches_etudiant/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Create directories for static and media
RUN mkdir -p /vol/web/static /vol/web/media

ENV STATIC_ROOT=/vol/web/static
ENV MEDIA_ROOT=/vol/web/media

# Collect static files (will be a no-op if STATIC_ROOT not configured in settings)
RUN python fiches_etudiant/manage.py collectstatic --noinput || true

EXPOSE 8000

# Default command: use gunicorn for production; you can override it in docker-compose for dev
CMD ["gunicorn", "fiches_etudiant.wsgi:application", "--bind", "0.0.0.0:8000"]
