# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:57

# 系统配置
from datetime import timedelta

# -------------------数据库配置-------------------
# 数据库配置：sqlite
# DB_URI = 'sqlite:///../flask_api.db'

# 数据库配置：mysql
USER = 'root'
PASSWORD = '123456'
HOST = 'localhost'
DB_NAME = 'flask_api'
DB_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}?charset=utf8'

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# -------------------数据库配置-------------------


# -------------------JWT-------------------
SECRET_KEY = "\x17wQ;\x0b\xbc4lj\xc2;$\xfc\x96$\xbc\x9e<\x07\x93\x97\x85S\x89G&\xfe\x97\xf8\x85Ip"
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 过期时间
# -------------------JWT-------------------
