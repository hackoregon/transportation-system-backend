#!/bin/bash
export PATH=$PATH:~/.local/bin

python manage.py migrate --noinput
python manage.py test --noinput
