#! /usr/bin/env bash

# Tear down docker environment after script is finished
trap "docker-compose down -v --remove-orphans" EXIT

# Exit in case of error
set -e

# Remove possibly previous broken stacks left hanging after an error
docker-compose down -v --remove-orphans

if [ $(uname -s) = "Linux" ]; then
    echo Remove __pycache__ files
    echo Check the source code before giving sudo powers to random scripts :P
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose build --build-arg INSTALL_DEV=true
docker-compose up -d
docker-compose exec -T backend bash /src/_tests_start.sh "$@"
