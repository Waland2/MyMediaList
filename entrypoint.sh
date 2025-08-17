#!/bin/bash

python3 manage.py migrate
python3 manage.py collectstatic --no-input
gunicorn mymedialist.wsgi:application --bind 0.0.0.0:8000