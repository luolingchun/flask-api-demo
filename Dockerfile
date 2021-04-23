FROM python:3.8-slim-buster

MAINTAINER LLC

# 使用上海时区
ENV TZ=Asia/Shanghai

# 拷贝依赖包文件
COPY requirements.txt /tmp/requirements.txt

# 基础环境安装
RUN \
    apt-get update -y && \
    apt-get install -y gcc && \
    \
    python -m pip install -r /tmp/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com && \
    python -m pip install supervisor uwsgi -i http://pypi.douban.com/simple --trusted-host pypi.douban.com && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.ini" >> /etc/supervisord.conf && \
    \
    apt-get purge -y gcc && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip/*

# 系统环境变量
ARG PROJECT_NAME

# 工作空间
WORKDIR /work/$PROJECT_NAME/src

# 程序部署
COPY bin /work/$PROJECT_NAME/bin
COPY src /work/$PROJECT_NAME/src
COPY conf/uwsgi.ini /work/$PROJECT_NAME/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/$PROJECT_NAME.ini


ENTRYPOINT ["supervisord", "-n","-c", "/etc/supervisord.conf"]