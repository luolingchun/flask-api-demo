# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/10/12 15:56

from app.rq import rq2

default_queue = rq2.get_queue('default')
