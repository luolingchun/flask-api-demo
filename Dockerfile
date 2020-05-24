FROM alpine:3.9

MAINTAINER LLC

COPY src /work/flask-api/src
COPY conf/uwsgi.ini /work/flask-api/conf/uwsgi.ini
COPY conf/supervisor.conf /etc/supervisord.d/flask-api.conf
COPY requirements.txt /tmp/requirements.txt

RUN echo "http://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories && \
    echo "http://mirrors.aliyun.com/alpine/v3.9/community/" >> /etc/apk/repositories && \
    \
    apk add --no-cache gcc python3 python3-dev linux-headers libc-dev && \
    apk add --no-cache bash bash-doc bash-completion && \
    \
    pip3 install -r /tmp/requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com && \
    pip3 install supervisor flask uwsgi -i http://pypi.douban.com/simple --trusted-host pypi.douban.com && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.conf" >> /etc/supervisord.conf && \
    \
    rm -rf /var/cache/apk/* && \
    rm -rf ~/.cache/pip

ENTRYPOINT ["supervisord", "-n","-c", "/etc/supervisord.conf"]