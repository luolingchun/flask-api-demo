# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 18:54
"""
全局异常处理
"""
import json

from flask import Response


class BaseAPIException(Response):
    status_code = 200
    code = -1
    message = '服务器未知错误'

    def __init__(self):
        super(BaseAPIException, self).__init__()
        self.response = json.dumps({"code": self.code, "message": self.message})
        self.status = self.status_code
        self.content_type = "application/json"


class UnknownException(BaseAPIException):
    code = 500


class ContentTypeException(BaseAPIException):
    code = -2
    message = "不支持的content-type类型"


class ParameterException(BaseAPIException):
    code = 1002
    message = "参数错误"


# -------------用户-------------
class UserExistException(BaseAPIException):
    code = 2001
    message = "用户已存在"


class UserNotExistException(BaseAPIException):
    code = 2002
    message = "用户不存在"


class PasswordException(BaseAPIException):
    code = 2003
    message = "密码错误"


class ActiveException(BaseAPIException):
    code = 2004
    message = "用户未激活"


class AuthException(BaseAPIException):
    code = 2005
    message = "认证失败，没有找到token"


class InvalidTokenException(BaseAPIException):
    code = 2006
    message = "token不合法"


class ExpiredTokenException(BaseAPIException):
    code = 2007
    message = "token已过期"


# -------------用户-------------


# -------------角色-------------
class RoleExistException(BaseAPIException):
    code = 3001
    message = "角色已存在"


class RoleNotExistException(BaseAPIException):
    code = 3002
    message = "角色不存在"


class RoleHasUserException(BaseAPIException):
    code = 3003
    message = "角色下存在用户，不可删除"
# -------------角色-------------
