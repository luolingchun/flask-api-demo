# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 17:33
from pydantic import BaseModel


def response(result: BaseModel):
    return result.dict()
