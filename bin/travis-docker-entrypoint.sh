#! /bin/bash

./manage.py collectstatic --noinput

gunicorn crash_data_api.wsgi -c gunicorn_config.py
