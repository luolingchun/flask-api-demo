
export PROJECT_NAME=flask-api-demo
# --no-cache
docker build --build-arg PROJECT_NAME -t "${PROJECT_NAME}:v1.0.0" .