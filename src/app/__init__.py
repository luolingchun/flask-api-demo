# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52

from flask_openapi3 import OpenAPI
from flask_openapi3.models import Info
from flask_openapi3.models.security import HTTPBearer


def register_apis(app: OpenAPI):
    """注册API蓝图"""
    # from app.api.user import api as user_api
    # from app.api.admin import api as admin_api
    from app.api.book import api as book_api
    # app.register_blueprint(user_api)
    # app.register_blueprint(admin_api)
    app.register_api(book_api)


def init_jwt(app: OpenAPI):
    """初始化JWT"""
    from app.utils.jwt_tools import jwt_manager
    jwt_manager.init_app(app)


def init_db(app: OpenAPI):
    """初始化数据库"""
    from app.models import db
    db.init_app(app)
    # db.create_all(app=app)


def create_app():
    from . import config
    # 创建Flask实例
    app = OpenAPI(
        __name__,
        info=Info(title=config.APP_NAME, version=config.APP_VERSION),
        securitySchemes={"jwt": HTTPBearer(bearerFormat="JWT")}
    )
    # 全局配置项
    app.config.from_object(config)
    # 初始化JWT
    init_jwt(app)
    # 初始化数据库
    init_db(app)
    # 注册蓝图
    register_apis(app)
    return app
