#! /bin/bash

echo Debug: $DEBUG


./manage.py collectstatic --noinput
./manage.py runserver 0.0.0.0:8000
