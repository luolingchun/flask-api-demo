# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:57
import os
from datetime import timedelta

APP_NAME = 'XXX API接口'

# -------------------数据库配置-------------------
mode = os.getenv('ENV', 'publish')
if mode == 'dev':
    # 数据库配置：sqlite
    DB_URI = "sqlite:////mnt/d/flask_api.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

else:
    # 数据库配置：mysql
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    DB_URI = f"pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}?charset=utf8"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = DB_URI
# -------------------数据库配置-------------------


# -------------------JWT-------------------
SECRET_KEY = "\x17wQ;\x0b\xbc4lj\xc2;$\xfc\x96$\xbc\x9e<\x07\x93\x97\x85S\x89G&\xfe\x97\xf8\x85Ip"
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 过期时间
# -------------------JWT-------------------
