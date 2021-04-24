# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11

from pydantic import BaseModel, Field
from spectree import SpecTree

from app.config import APP_NAME

spec = SpecTree("flask", TITLE=APP_NAME, VERSION="1.0", MODE="strict")


class JsonResponse(BaseModel):
    code: int = Field(default=0)
    message: str = Field(default='ok')
