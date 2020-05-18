# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 17:33


def response(code, message, **kwargs):
    data = {"code": code, "message": message}
    data.update(**kwargs)
    return data
