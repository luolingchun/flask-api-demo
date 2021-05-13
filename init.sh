
PROJECT_NAME=$1

if [ "${PROJECT_NAME}" = "" ]
  then
    echo "PROJECT_NAME is not set"
    echo "eg: sh init.sh cms-server"
    exit 1
fi

export DEFAULT_NAME=flask-api-demo

sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./docker-compose.yml
sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./build.sh
sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./README.md