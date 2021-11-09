# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 15:04

from pydantic import BaseModel, Field


class BookBody(BaseModel):
    name: str = Field(..., description='名称')
    author: str = Field(None, description='作者')


class BookQuery(BaseModel):
    id: int = Field(..., description='图书id')
