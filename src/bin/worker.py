# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 10:22
from app.rq import rq2
from wsgi import app

with app.app_context():
    default_worker = rq2.get_worker('default')
    # default_worker.work(burst=True) #全部任务完成后退出
    default_worker.work()
