# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer

db = SQLAlchemy()


class Base(db.Model):
    """基础数据库模型：提供id、创建时间、更新时间"""
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    create_time = Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)