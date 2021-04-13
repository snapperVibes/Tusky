#!/usr/bin/env bash
# Exit on error
set -e

# Assuming you are running from .../tusky
CODEGEN_DIR=${PWD}/frontend/src/_generated_code

# Download the api
wget http://localhost:8000/openapi.json -O $CODEGEN_DIR/openapi.json --quiet

# Ensure /gen exists
ls /gen || {
    echo To use this script, the folder /gen has to exist.
    sudo mkdir /gen
}

docker run \
        --rm \
        --volume $CODEGEN_DIR:/local \
    swaggerapi/swagger-codegen-cli-v3 generate \
        --lang typescript-axios \
        --input-spec /local/openapi.json \
        --output /local

# Todo: Get working on Windows
#npm run --prefix $CODEGEN_DIR lint
