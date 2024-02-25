# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 10:22
from rq import Worker

from app.config import REDIS_CONNECT
from wsgi import app

with app.app_context():
    worker = Worker(queues="default", connection=REDIS_CONNECT)
    # worker.work(burst=True) #全部任务完成后退出
    worker.work()
