# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from . import config
from app.utils.exceptions import APIException, UnknownException


def init_exception(app: Flask):
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
                app.logger.error(traceback.format_exc())
                return UnknownException()
            else:
                raise e


def register_blueprints(app: Flask):
    """注册蓝图"""
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def init_db(app: Flask):
    """初始化数据库"""
    from app.models.base import db
    db.init_app(app)


def create_app():
    # 创建Flask示例
    app = Flask(__name__)
    # 配置项
    app.config.from_object(config)
    # 跨域支持
    CORS(app)
    # 初始化全局异常
    init_exception(app)
    # 注册蓝图
    register_blueprints(app)
    # 初始化数据库
    init_db(app)
    return app