# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 15:04
from typing import Optional

from pydantic import BaseModel, Field


class QueryBook(BaseModel):
    page: int = Field(default=0, ge=0, description='页码')
    page_size: int = Field(default=15, ge=0, description='每页个数')


class CreateBook(BaseModel):
    name: str = Field(description='图书名称')
    author: Optional[str] = Field(description='作者')
