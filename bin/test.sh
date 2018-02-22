#! /bin/bash
usage() { echo "Usage: $0 [-l] for a local test, [-s] for a local staging test, or [-t] for a travis test " 1>&2; exit 1; }

while getopts ":lst" opt; do
    case "$opt" in
        l)
          docker-compose -p tests run --entrypoint /code/bin/test-entrypoint.sh  -p 8000 --rm api
          echo "Stopping test db container"
          docker stop tests_db_1
          echo "Removing test db container"
          docker rm tests_db_1
           ;;
        s)
          docker-compose -p tests run --entrypoint /code/bin/test-entrypoint.sh  -p 8000 --all -f
          echo "Stopping test db container"
          docker stop tests_db_1
          echo "Removing test db container"
          docker rm tests_db_1
          ;;
        t)
          docker-compose -f travis-docker-compose.yml run \
          --entrypoint /code/bin/test-entrypoint.sh
          ;;
        *)
          usage
          ;;
    esac
done
