# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint
from app.api.v1 import user, book


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    # 红图注册
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    return bp_v1
