FROM python:3.9-slim-bullseye

LABEL author="LLC"

# 使用上海时区
ENV TZ=Asia/Shanghai

# 拷贝依赖包文件
COPY requirements.txt /tmp/requirements.txt

# 基础环境安装
RUN \
    set -ex && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free">> /etc/apt/sources.list  && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free">> /etc/apt/sources.list  && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free">> /etc/apt/sources.list  && \
    \
    apt-get update && \
    apt-get install -y gcc python3-dev --no-install-recommends && \
    \
    pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    uv pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    uv pip install supervisor uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.ini" >> /etc/supervisord.conf && \
    \
    apt-get purge -y gcc  python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip/*

# 解决中文环境问题
RUN apt-get update && \
    apt-get install -y language-pack-zh-hans  && \
    locale-gen zh_CN.UTF-8 && update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8

ENV LANG='zh_CN.UTF-8'
ENV LANGUAGE='zh_CN:zh:en_US:en'
ENV LC_ALL='zh_CN.UTF-8'

# 工作空间
WORKDIR /work/src

# 添加pythonpath
ENV PYTHONPATH=/work/src

# 程序部署
COPY conf/uwsgi.ini /work/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/supervisor.ini
COPY src /work/src


ENTRYPOINT ["supervisord", "-n","-c", "/etc/supervisord.conf"]