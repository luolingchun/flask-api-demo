# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/14 9:33
from flask_openapi3 import FileStorage
from pydantic import BaseModel, Field


class UploadFileForm(BaseModel):
    file: FileStorage
    file_type: str = Field(None, description="文件类型")


class DownloadFilePath(BaseModel):
    filename: str = Field(None, description="文件名称")
