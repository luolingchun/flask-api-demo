# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52
import traceback

from flask_openapi3 import HTTPBearer
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix


def init_exception(app: OpenAPI):
    from app.utils.exceptions import BaseAPIException, UnknownException

    @app.errorhandler(Exception)
    def handler(e):
        """处理全局异常"""
        if isinstance(e, BaseAPIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            message = e.description
            return BaseAPIException(code, message)
        else:
            print(traceback.format_exc())
            return UnknownException()


def register_apis(app: OpenAPI):
    """注册API蓝图"""
    from app.api.user import api as user_api
    from app.api.admin import api as admin_api
    from app.api.book import api as book_api
    from app.api.file import api as file_api
    from app.api.job import api as job_api
    app.register_api(user_api)
    app.register_api(admin_api)
    app.register_api(book_api)
    app.register_api(file_api)
    app.register_api(job_api)


def init_jwt(app: OpenAPI):
    """初始化JWT"""
    from app.utils.jwt_tools import jwt_manager
    jwt_manager.init_app(app)


def init_db(app: OpenAPI):
    """初始化数据库"""
    from app.model import db
    db.init_app(app)


def init_rq2(app: OpenAPI):
    """初始化rq2"""
    from app.rq import rq2
    rq2.init_app(app)


def create_app():
    from . import config
    # 创建Flask实例
    app = OpenAPI(
        __name__,
        info=Info(title=config.APP_NAME, version=config.APP_VERSION),
        security_schemes={"jwt": HTTPBearer(bearerFormat="JWT")}
    )
    # 使用真实IP
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # 全局配置项
    app.config.from_object(config)
    # 初始化全局异常
    init_exception(app)
    # 初始化JWT
    init_jwt(app)
    # 初始化数据库
    init_db(app)
    # 初始化rq2
    init_rq2(app)
    # 注册API蓝图
    register_apis(app)
    return app
