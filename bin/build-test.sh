#! /bin/bash
usage() { echo "Usage: $0 [-l] for a local test or [-t] for a travis test " 1>&2; exit 1; }

while getopts ":lt" opt; do
    case "$opt" in
        l)
          docker-compose -f docker-compose.yml build
          docker-compose -p tests run --entrypoint /code/bin/test-entrypoint.sh  -p 8000 --rm api
           ;;
        t)
          docker-compose -f travis-docker-compose.yml build
          docker-compose -f travis-docker-compose.yml run \
          --entrypoint /code/bin/test-entrypoint.sh
          ;;
        *)
          usage
          ;;
    esac
done
