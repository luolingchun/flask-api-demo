# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 18:54
from flask import json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 200
    error_code = -1
    message = '服务器未知错误'

    def __init__(self, code=None, message=None, error_code=None, headers=None):
        if code:
            self.code = code
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if headers is not None:
            headers_merged = headers.copy()
            headers_merged.update(self.headers)
            self.headers = headers_merged

        super(APIException, self).__init__(message, None)

    def get_body(self, environ=None):
        body = {
            "code": self.error_code,
            "message": self.message,
        }
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class UnknownException(APIException):
    code = 500


class ContentTypeException(APIException):
    error_code = -2
    message = "不支持的content-type类型"


class ParameterException(APIException):
    error_code = 1002
    message = "参数错误"


# -------------用户-------------
class UserExistException(APIException):
    error_code = 2001
    message = "用户已存在"


class UserNotExistException(APIException):
    error_code = 2002
    message = "用户不存在"


class PasswordException(APIException):
    error_code = 2003
    message = "密码错误"


class ActiveException(APIException):
    error_code = 2004
    message = "用户未激活"


class AuthException(APIException):
    error_code = 2005
    message = "认证失败，没有找到token"


class InvalidTokenException(APIException):
    error_code = 2006
    message = "token不合法"


class ExpiredTokenException(APIException):
    error_code = 2007
    message = "token已过期"


# -------------用户-------------


# -------------角色-------------
class RoleExistException(APIException):
    error_code = 3001
    message = "角色已存在"


class RoleNotExistException(APIException):
    error_code = 3002
    message = "角色不存在"


class RoleHasUserException(APIException):
    error_code = 3003
    message = "角色下存在用户，不可删除"
# -------------角色-------------
