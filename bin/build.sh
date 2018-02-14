#! /bin/bash
usage() { echo "Usage: $0 [-l] for a local build, [-s] for a local staging build, or [-t] for a travis build " 1>&2; exit 1; }

while getopts ":lst" opt; do
    case "$opt" in
        l)
          docker-compose -f docker-compose.yml build
          ;;
        s)
          docker-compose -f staging-docker-compose.yml build
          ;;
        t)
          docker-compose -f travis-docker-compose.yml build
          ;;
        *)
          usage
          ;;
    esac
done
