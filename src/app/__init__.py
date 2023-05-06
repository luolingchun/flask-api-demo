# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52
import importlib
import os
import re
import traceback
from flask_cors import CORS
from flask_openapi3 import HTTPBearer, HTTPBase
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


def auto_register_api(app: OpenAPI):
    """自动注册蓝图API
    自动寻找api文件夹中的APIBlueprint并完成注册
    """
    here = os.path.dirname(__file__)
    api_dir = os.path.join(here, "api")
    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file == "__init__.py":
                continue
            if not file.endswith(".py"):
                continue
            api_file = os.path.join(root, file)
            rule = re.split(r"src|.py", api_file)[1]
            api_route = ".".join(rule.split(os.sep)).strip(".")
            try:
                api = importlib.import_module(api_route)
                app.register_api(api.api)
            except AttributeError:
                print(f"模块 {api_route} 中没有api变量")
            except:
                traceback.print_exc()
                print(f"模块 {api_route} 自动注册错误")


def register_apis(app: OpenAPI):
    """注册API蓝图"""
    # from app.api.user import api as user_api
    # from app.api.admin import api as admin_api
    # from app.api.book import api as book_api
    # from app.api.file import api as file_api
    # from app.api.job import api as job_api
    # app.register_api(user_api)
    # app.register_api(admin_api)
    # app.register_api(book_api)
    # app.register_api(file_api)
    # app.register_api(job_api)
    auto_register_api(app)


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
        security_schemes={
            "basic": HTTPBase(),
            "jwt": HTTPBearer(bearerFormat="JWT")
        },
        doc_expansion="none",
    )
    # json 正确返回中文
    app.json.ensure_ascii = False
    # 使用真实IP
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    # 全局配置项
    app.config.from_object(config)
    # 初始化全局异常
    init_exception(app)
    # 跨域支持
    CORS(app)
    # 初始化JWT
    init_jwt(app)
    # 初始化数据库
    init_db(app)
    # 初始化rq2
    init_rq2(app)
    # 注册API蓝图
    register_apis(app)
    return app
