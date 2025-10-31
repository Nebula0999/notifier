#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to Django project directory
cd finance_alert

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create superuser if needed (optional - comment out if not needed)
# python manage.py createsuperuser --no-input --username admin --email admin@example.com
