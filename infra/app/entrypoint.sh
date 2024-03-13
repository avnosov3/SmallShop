#!/bin/bash

python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py createsuperuserauto

gunicorn core.wsgi --bind 0:8000
