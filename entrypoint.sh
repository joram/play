#!/bin/sh

PORT=${PORT:-8000}
WORKERS=${WORKERS:-3}

./manage.py migrate
./manage.py collectstatic

exec gunicorn wsgi:application --bind "0.0.0.0:$PORT" --workers "$WORKERS"
