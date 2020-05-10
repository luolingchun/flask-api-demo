# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import inspect, Column, Integer, orm


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()


class Base(db.Model):
    """基础数据库模型：提供id、创建时间、更新时间"""
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    create_time = Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
