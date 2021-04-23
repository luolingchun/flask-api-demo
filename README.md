# flask-api-demo

## 项目初始化

修改`init_project.sh`中的PROJECT_NAME，并执行`init_project.sh`

## 开发说明

1. 修改`build.sh`和`docker-compose.yml`中镜像版本，执行`build.sh`构建镜像
2. 执行`docker-compose up -d`启动容器
3. 执行`docker exec -it flask-api-demo bash`进入容器
4. 执行`supervisorctl stop app`停止服务，并执行`python manage.py runserver`进入开发者模式
5. 调试完成后执行`build.sh`构建发布镜像

## 版本

### v1.0.0 2021-04-23

- 初始版本