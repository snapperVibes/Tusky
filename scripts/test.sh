#! /usr/bin/env bash
trap "docker-compose down -v --remove-orphans" EXIT


# Exit in case of error
set -e

docker-compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose build
docker-compose up -d
# This is really ugly, use _wait_for_it.sh
./scripts/_wait_for_it.sh -t 8 localhost:8000
docker-compose exec -T web bash /src/scripts/_tests_start.sh "$@"
