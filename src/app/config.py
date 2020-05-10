# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:57

# 数据库配置

# sqlite
db_uri = 'sqlite:///flask_api.db'

# mysql
user = 'root'
password = '123456'
ip = 'localhost'
db_name = 'flask_api'
# db_uri = f'mysql://{user}:{password}@{ip}/{db_name}?charset=utf8'

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 密钥
SECRET_KEY = "\x17wQ;\x0b\xbc4lj\xc2;$\xfc\x96$\xbc\x9e<\x07\x93\x97\x85S\x89G&\xfe\x97\xf8\x85Ip"
