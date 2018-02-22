#!/bin/bash
export PATH=$PATH:~/.local/bin


set -e

export PGPASSWORD=$POSTGRES_PASSWORD
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -p "$POSTGRES_PORT" -d postgres -c '\q'
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 15
done

>&2 echo "Postgres is up"
# echo Debug: $DEBUG

# Collect static files

# echo "Migrate"
# ./manage.py migrate


./manage.py test --nomigrations
