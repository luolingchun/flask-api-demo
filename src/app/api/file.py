# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/26 16:56
import os

from flask import make_response, send_file
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import API_PREFIX, FILE_PATH
from app.form.file import UploadFile, DownloadFile

__version__ = '/v1'
__bp__ = '/file'

from app.utils.exceptions import FileNotExistException

api = APIBlueprint(__bp__, __name__, url_prefix=API_PREFIX + __version__ + __bp__)

tag = Tag(name=__version__ + __bp__, description="文件")


@api.post('/upload', tags=[tag])
def upload_file(form: UploadFile):
    """上传文件"""
    print(form.file.filename)
    print(form.file_type)
    form.file.save(os.path.join(FILE_PATH, 'test.jpg'))
    return {"code": 0, "message": "ok"}


@api.get('/<filename>', tags=[tag])
def download_file(path: DownloadFile):
    """下载文件"""
    file = os.path.join(FILE_PATH, path.filename)
    if os.path.exists(file):
        return make_response(send_file(file, as_attachment=True, cache_timeout=60))
    raise FileNotExistException()


@api.get('/image/<filename>', tags=[tag])
def get_image(path: DownloadFile):
    """获取图片流"""
    image_content = b''
    try:
        file = os.path.join(FILE_PATH, path.filename)
        with open(file, 'rb') as f:
            image_content = f.read()
    except Exception as e:
        print(e)
    r = make_response(image_content)
    r.headers['Content-Type'] = 'image/jpeg'

    return r
