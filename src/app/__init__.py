# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException


def init_exception(app: Flask):
    from app.utils.exceptions import APIException, UnknownException

    @app.errorhandler(Exception)
    def handler(e):
        """处理全局异常"""
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            message = e.description
            return APIException(code, message)
        else:
            traceback.print_exc()
            return UnknownException()


def register_blueprints(app: Flask):
    """注册蓝图"""
    from app.api.user import api as user_api
    from app.api.admin import api as admin_api
    from app.api.book import api as book_api
    # app.register_blueprint(user_api)
    # app.register_blueprint(admin_api)
    app.register_blueprint(book_api)


def init_jwt(app):
    """初始化JWT"""
    from app.utils.jwt_tools import jwt_manager
    jwt_manager.init_app(app)


def init_db(app: Flask):
    """初始化数据库"""
    from app.models import db
    db.init_app(app)
    # db.create_all(app=app)


def init_spec(app: Flask):
    """初始化API文档"""
    from app.specs import spec
    spec.register(app)


def create_app():
    from . import config
    # 创建Flask实例
    app = Flask(__name__)
    # 全局配置项
    app.config.from_object(config)
    # openapi文档
    init_spec(app)
    # 初始化全局异常
    init_exception(app)
    # 初始化JWT
    init_jwt(app)
    # 初始化数据库
    init_db(app)
    # 注册蓝图
    register_blueprints(app)
    return app
