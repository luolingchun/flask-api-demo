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
    error_code = 1001
    message = "不支持的content-type类型"


class ParameterException(APIException):
    error_code = 1002
    message = "参数错误"
