# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2022/10/28 16:31
from functools import wraps

from flask import request

from app.config import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD
from app.utils.exceptions import PasswordException


def basic_required(func):
    """HTTP Basic装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth:
            is_passed = (auth.username == BASIC_AUTH_USERNAME and auth.password == BASIC_AUTH_PASSWORD)
        else:
            is_passed = False
        if not is_passed:
            raise PasswordException()
        return func(*args, **kwargs)

    return wrapper
