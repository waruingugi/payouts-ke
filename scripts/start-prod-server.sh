#!/bin/sh
python manage.py collectstatic --no-input
gunicorn payouts.wsgi --bind 0.0.0.0:8000 --timeout 60 --access-logfile - --error-logfile -
