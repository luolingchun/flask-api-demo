# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24
import math
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select, Column, and_, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase

from app.utils.exceptions import ResourceExistException


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_offset_limit(page, page_size):
    """获取页码偏移量"""
    page = 1 if page < 1 else page
    limit = page_size
    offset = (page - 1) * limit
    return offset, limit


def get_total_page(_id, condition, limit):
    """获取总个数、总页数"""
    total = db.session.execute(select(func.count(_id)).where(*condition)).scalar()
    total_page = math.ceil(total / limit)
    return total, total_page


def validate_name(model, key, value, message="名称"):
    # 高并发场景下会失效
    if db.session.execute(select(model).where(and_(key == value))).first():
        raise ResourceExistException(message=f"{message}已存在")


def validate_name_when_update(model, model_id, key, value, message="名称"):
    # 高并发场景下会失效
    if db.session.execute(select(model).where(and_(model.user_id != model_id, key == value))).scalar():
        raise ResourceExistException(message=f"{message}已存在")


class Base(db.Model):
    """基础数据库模型：提供id、创建时间、更新时间"""
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
