# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24
import math
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, func

db = SQLAlchemy()


def get_offset_limit(page, page_size):
    """获取页码偏移量"""
    limit = page_size
    offset = (page - 1) * limit
    return offset, limit


def get_total_page(model, condition, limit):
    """获取总个数、总页数"""
    total = db.session.query(func.count(model.id)).filter(*condition).scalar()
    total_page = math.ceil(total / limit)
    return total, total_page


class Base(db.Model):
    """基础数据库模型：提供id、创建时间、更新时间"""
    __abstract__ = True
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}  # 支持中文
    id = Column(Integer, primary_key=True)
    create_time = Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
