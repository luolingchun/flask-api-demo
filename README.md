# flask-api-demo

## 项目初始化

执行`sh init.sh PROJECT_NAME`

## 开发说明

1. 修改`build.sh`和`docker-compose.yml`中镜像版本，执行`build.sh`构建镜像
2. 执行`docker-compose up -d`启动容器
3. 执行`docker exec -it flask-api-demo bash`进入容器
4. 执行`supervisorctl stop app`停止服务，并执行`flask run`进入开发者模式
5. 重新执行第一步发布镜像

## 部署说明

1. 准备`docker-compose.yml`, 删除源码挂载：`- "./:/work"`

2. 启动服务：`docker-compose up -d`

3. 数据库迁移：

    1. docker exec -it flask-api-demo bash
    2. flask db init -d /data/data/migrations
    3. flask db migrate -d /data/data/migrations
    4. flask db upgrade -d /data/data/migrations

4. 初始化数据库：

   ```bash
   flask init_db
   ```

