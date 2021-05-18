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
    python -m pip install -U pip && \
    python -m pip install -r /tmp/requirements.txt && \
    python -m pip install supervisor uwsgi && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.ini" >> /etc/supervisord.conf && \
    \
    apt-get purge -y gcc && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip/*


# 工作空间
WORKDIR /work/src

# 添加pythonpath
ENV PYTHONPATH=/work/src

# 程序部署
COPY src /work/src
COPY conf/uwsgi.ini /work/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/supervisor.ini


ENTRYPOINT ["supervisord", "-n","-c", "/etc/supervisord.conf"]