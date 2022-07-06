# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/12 15:36
from . import Base, db


class Book(Base):
    __tablename__ = "book"
    __table_args__ = ({"comment": "图书表"})
    name = db.Column(db.String(32), comment="名称")
    author = db.Column(db.String(4), comment="作者")
