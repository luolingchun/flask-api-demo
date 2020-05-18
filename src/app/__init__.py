# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52

from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.utils.jwt import jwt


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
            if not app.config['DEBUG']:
                import traceback
                traceback.format_exc()
                return UnknownException()
            else:
                raise e


def register_blueprints(app: Flask):
    """注册蓝图"""
    from app.api.user import api as user_api
    from app.api.admin import api as admin_api
    from app.api.book import api as book_api
    app.register_blueprint(user_api)
    app.register_blueprint(admin_api)
    app.register_blueprint(book_api)


def init_jwt(app):
    jwt.init_app(app)


def init_db(app: Flask):
    """初始化数据库"""
    from app.models.base import db
    db.init_app(app)
    # db.create_all(app=app)


def create_app():
    from . import config
    # 创建Flask示例
    app = Flask(__name__)
    # 配置项
    app.config.from_object(config)
    # swagger 文档
    Swagger(app, config=config.SWAGGER_CONFIG)
    # 跨域支持
    CORS(app)
    # 初始化全局异常
    init_exception(app)
    # 初始化JWT
    init_jwt(app)
    # 初始化数据库
    init_db(app)
    # 注册蓝图
    register_blueprints(app)
    return app
