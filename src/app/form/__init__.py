# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11

from pydantic import BaseModel, Field


class JsonResponse(BaseModel):
    code: int = Field(default=0, description="状态码")
    message: str = Field(default='ok', description="异常信息")
