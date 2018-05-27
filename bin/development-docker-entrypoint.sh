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
echo Debug: $DEBUG
# Collect static files
echo "Collect static files"
./manage.py collectstatic --noinput

echo "Make migrations"
./manage.py makemigrations

echo "Migrate"
./manage.py migrate

echo "Run server..."
./manage.py runserver 0.0.0.0:8000
