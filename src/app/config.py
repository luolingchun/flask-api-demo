# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:57
import os
from datetime import timedelta

# -------------------APP基础配置-------------------
APP_NAME = "Flask API"
APP_VERSION = "1.0.0"
API_PREFIX = "/api"
# -------------------APP基础配置-------------------

# 正确返回中文
JSON_AS_ASCII = False

# -------------------数据库配置-------------------
# 数据库配置：postgres
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


# -------------------redis数据库配置-------------------
REDIS_HOST = os.getenv("REDIS_HOST", "flask-redis")
REDIS_USER = os.getenv("REDIS_USER", "redis_user")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "redis_password")
REDIS_PORT = 6379
RQ_REDIS_DB = 0
RQ_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{RQ_REDIS_DB}"
# -------------------redis数据库配置-------------------

# -------------------HTTP Basic-------------------
BASIC = [{"basic": []}]
BASIC_AUTH_USERNAME = "admin"
BASIC_AUTH_PASSWORD = "admin123"
# -------------------HTTP Basic-------------------

# -------------------JWT-------------------
JWT = [{"jwt": []}]
JWT_SECRET_KEY = "hard to guess"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 过期时间
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
# -------------------JWT-------------------


# -------------------数据路径-------------------
DATA_PREFIX = "/data/data"
FILE_PATH = os.path.join(DATA_PREFIX, "files")
for d in [FILE_PATH]:
    if not os.path.exists(d):
        os.makedirs(d)
# -------------------数据路径-------------------
