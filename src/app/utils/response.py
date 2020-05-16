# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 17:33


def response(code, message, data=None):
    if data is None:
        return {
            "code": code,
            "message": message,
        }
    else:
        return {
            "code": code,
            "message": message,
            "data": data,
        }
