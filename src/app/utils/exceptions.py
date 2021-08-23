# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 18:54
"""
全局异常处理
"""
import json

from werkzeug.exceptions import HTTPException


class BaseAPIException(HTTPException):
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

        super(BaseAPIException, self).__init__(message, None)

    def get_body(self, *args, **kwargs):
        body = {
            "code": self.error_code,
            "message": self.message,
        }
        text = json.dumps(body, ensure_ascii=False)
        return text

    def get_headers(self, *args, **kwargs):
        return [('Content-Type', 'application/json')]


class UnknownException(BaseAPIException):
    code = 500


class ContentTypeException(BaseAPIException):
    error_code = -2
    message = "不支持的content-type类型"


class ParameterException(BaseAPIException):
    error_code = 1002
    message = "参数错误"


# -------------用户-------------
class UserExistException(BaseAPIException):
    error_code = 2001
    message = "用户已存在"


class UserNotExistException(BaseAPIException):
    error_code = 2002
    message = "用户不存在"


class PasswordException(BaseAPIException):
    error_code = 2003
    message = "密码错误"


class ActiveException(BaseAPIException):
    error_code = 2004
    message = "用户未激活"


class AuthException(BaseAPIException):
    error_code = 2005
    message = "认证失败，没有找到token"


class InvalidTokenException(BaseAPIException):
    error_code = 2006
    message = "token不合法"


class ExpiredTokenException(BaseAPIException):
    error_code = 2007
    message = "token已过期"


class EmailExistException(BaseAPIException):
    error_code = 2008
    message = "邮箱已被注册"


# -------------用户-------------


# -------------角色-------------
class RoleExistException(BaseAPIException):
    error_code = 3001
    message = "角色已存在"


class RoleNotExistException(BaseAPIException):
    error_code = 3002
    message = "角色不存在"


class RoleHasUserException(BaseAPIException):
    error_code = 3003
    message = "角色下存在用户，不可删除"


# -------------角色-------------

# -------------文件-------------
class ResourceNotExistException(BaseAPIException):
    error_code = 4001
    message = "文件不存在"


# -------------文件-------------

# -------------任务-------------
class JobNotExistException(BaseAPIException):
    error_code = 5001
    message = "任务不存在"


class JobNotRetryException(BaseAPIException):
    error_code = 5002
    message = "只能重试执行失败的任务"


class JobTypeErrorException(BaseAPIException):
    error_code = 5003
    message = "任务类型无效"


class OneClickErrorException(BaseAPIException):
    error_code = 5004
    message = "一键任务为空"

# -------------任务-------------
