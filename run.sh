#!/bin/bash
python manage.py collectstatic --noinput &&
python manage.py makemigrations &&
python manage.py migrate &&
gunicorn tianji.wsgi:application -c gunicorn.conf.py