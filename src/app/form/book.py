# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 15:04
from typing import Optional, List

from pydantic import BaseModel, Field


class CreateBook(BaseModel):
    name: str = Field(..., description='名称')
    author: str = Field(None, description='作者')


class QueryBook(BaseModel):
    page: int = Field(default=1, ge=1, description='页码')
    page_size: int = Field(default=15, ge=1, description='每页个数')
