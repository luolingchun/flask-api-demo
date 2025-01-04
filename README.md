# flask-api-demo

## 项目初始化

执行`sh init.sh PROJECT_NAME`

## 开发说明

1. 修改`build.sh`和`docker-compose.yml`中镜像版本，执行`sh build.sh`构建镜像
2. 执行`docker-compose up -d`启动容器
3. 执行`docker exec -it flask-api-demo bash`进入容器
4. 执行`supervisorctl stop webapp`停止服务，并执行`flask run`或`python wsgi.py`进入开发者模式
5. 在`CHANGELOG.md`中记录版本日志，重新执行第一步发布镜像

## 运维调试

1. 进入容器后使用`supervisorctl status`进程状态

   ```bash
   # supervisorctl status
   webapp                              RUNNING   pid 8, uptime 3 days, 5:35:50
   worker                           RUNNING   pid 10, uptime 3 days, 5:35:50
   ```
   
2. 停止进程：`supervisorctl stop webapp`
3. 启动进程：`supervisorctl start webapp`
4. 查看日志：`tail -f /data/log/webapp.log`
5. 查看日志：`tail -f /data/log/worker.log`

## 部署说明

1. 创建`flask`网络：`docker network create flask`

   可能遇到网络冲突问题，解决方法：
   1. 删除网络：`docker network rm flask`
   2. 创建网络时指定掩码和网关：
   
      `docker network create --subnet=192.168.0.0/24 --gateway=192.168.0.1 flask`

2. 准备`docker-compose.yml`, 注释源码挂载：`- "./:/work"`

3. 启动服务：`docker-compose up -d`

4. 数据库迁移：

    1. docker exec -it flask-api-demo bash
    2. flask db init -d /data/data/migrations
    3. flask db migrate -d /data/data/migrations
    4. flask db upgrade -d /data/data/migrations

5. 初始化数据库：

   ```bash
   flask init_db
   ```

## Docker配置文件

1. vim /etc/docker/daemon.json
   
   - default-runtime：修改默认运行时为nvidia
   - data-root：修改数据存储路径
   - bip：修改网卡地址
   
   ```json
   {
       "default-runtime": "nvidia",
       "runtimes": {
           "nvidia": {
               "path": "nvidia-container-runtime",
               "runtimeArgs": []
           }
       },
       "data-root":"/data/docker_data",
       "bip":"192.168.0.1/24"
   }
   ```