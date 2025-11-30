#!/bin/bash
# Run script for Django application

# Run migrations
python manage.py migrate

# Collect static files (optional, for production)
python manage.py collectstatic --noinput || true

# Start Django development server
python manage.py runserver 0.0.0.0:8000

