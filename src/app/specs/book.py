# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 15:04
from typing import Optional, List

from pydantic import BaseModel, Field

from . import JsonResponse


# ----------------------Request----------------------
class QueryBook(BaseModel):
    page: int = Field(default=1, ge=1, description='页码')
    page_size: int = Field(default=15, ge=1, description='每页个数')


class CreateBook(BaseModel):
    name: str = Field(description='图书名称')
    author: Optional[str] = Field(description='作者')


# ----------------------Request----------------------


# ----------------------Response---------------------
class Book(BaseModel):
    id: int = Field(description='图书ID')
    name: str = Field(description='图书名称')
    authors: List[str] = Field(description="作者")


class QueryBookResponse(JsonResponse):
    data: Book
# ----------------------Response---------------------
