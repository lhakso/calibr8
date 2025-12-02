#!/bin/bash
# Azure App Service startup script

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate --no-input

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 backend.wsgi
