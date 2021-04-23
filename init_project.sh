
export PROJECT_NAME=flask_test

export DEFAULT_NAME=flask-api-demo

sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./conf/supervisor.ini
sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./conf/uwsgi.ini
sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./docker-compose.yml
sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./build.sh