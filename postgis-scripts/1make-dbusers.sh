#! /bin/bash

# create the user we'll be restoring to!
if [ "$DATABASE_OWNER" = "postgres" ]
then
  echo "'postgres' already exists - exiting normally"
else
  echo "Creating database user '$DATABASE_OWNER'"
  createuser --no-createdb --no-createrole --no-superuser --no-replication $DATABASE_OWNER
  command="ALTER USER \"$DATABASE_OWNER\" WITH PASSWORD '${TEAM_PASSWORD}';"
  psql -c "$command"
fi
