# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2024/6/11 9:48
from pydantic import BaseModel, Field


class CreatePOIBody(BaseModel):
    name: str = Field(..., description="名称")
    lng: float = Field(..., description="经度")
    lat: float = Field(..., description="纬度")
