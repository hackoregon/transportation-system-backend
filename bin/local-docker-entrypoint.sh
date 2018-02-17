#! /bin/bash

# wait-for-postgres.sh
# https://docs.docker.com/compose/startup-order/

set -e

export PGPASSWORD=$POSTGRES_PASSWORD
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -p "$POSTGRES_PORT" -d postgres -c '\q'
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 15
done

>&2 echo "Postgres is up"

python manage.py migrate
./manage.py runserver 0.0.0.0:8000
