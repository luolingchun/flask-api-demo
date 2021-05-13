# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:57
import os
from datetime import timedelta

# -------------------APP基础配置-------------------
APP_NAME = "Flask API"
APP_VERSION = "1.0.0"
API_PREFIX = '/api'
# -------------------APP基础配置-------------------


# -------------------数据库配置-------------------
# 数据库配置：postgre
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "123456")
PG_DB = os.getenv("PG_DB", "flask")
PG_HOST = os.getenv("PG_HOST", "flask-postgres")
PG_PORT = os.getenv("PG_PORT", 5432)
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
if not bool(int(os.getenv("DEV", 0))):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = DB_URI
# -------------------数据库配置-------------------


# -------------------JWT-------------------
JWT = [{"jwt": []}]
JWT_SECRET_KEY = "hard to guess"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 过期时间
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
# -------------------JWT-------------------
