#! /bin/bash
usage() { echo "Usage: $0 [-d] for a development test, [-p] for production test" 1>&2; exit 1; }

if [ $# == 0 ]; then usage; fi

while getopts ":dp" opt; do
    case "$opt" in
        d)
          docker-compose -f development-docker-compose.yml run --entrypoint /code/bin/test-entrypoint.sh  api_development
           ;;
        p)
          docker-compose -f production-docker-compose.yml run --entrypoint /code/bin/test-entrypoint.sh  $DOCKER_SERVICE
          ;;
        *)
          usage
          ;;
    esac
done
