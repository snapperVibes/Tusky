#!/usr/bin/env bash
# Generates Javascript code in tusky/frontend/src/_generated_code
#  based on the OpenAPI (Swagger) standard.
#  Assumes Docker is installed and the backend is running on port 8000


# Exit on error
set -e

CODEGEN_DIR=${PWD}/frontend/src/_generated_code

# Download the api
# Todo: Add error handling, namely for is this step fails
wget http://localhost:8000/openapi.json -O $CODEGEN_DIR/openapi.json

# Ensure /gen exists
ls /gen || {
    echo Create /gen
    echo Check the source code before giving sudo powers to random scripts.
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

# When this script was written, swagger-codegen-cli-v3 contained an error;
#   ```
#   ERROR in src/_generated_code/apis/quizzes-api.ts:20:10
#   Module '"../models"' has no exported member 'ModelObject'.
#   ```
#  This is a quick fix and should be removed whenever the docker-container actually
#
#  If anyone has more information on the bug, please file a bug report.
#  I don't have enough confidence that it isn't caused by
#  something I wrote that doesn't follow the OpenApi spec.
echo "Adding 'export class ModelObject{} to $CODEGEN_DIR/models/index.ts'"
echo "export class ModelObject{}" >> $CODEGEN_DIR/models/index.ts
echo "Changing BASE_PATH to http://localhost:8000 in $CODEGEN_DIR/base.ts"
sed -i '/export const BASE_PATH/cexport const BASE_PATH = "http://localhost:8000";' $CODEGEN_DIR/base.ts
