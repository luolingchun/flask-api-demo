# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/26 16:56
import os

from flask import make_response, send_file
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import API_PREFIX, FILE_PATH
from app.form.file import UploadFileForm, DownloadFilePath
from app.utils.exceptions import FileNotExistException

__version__ = '/v1'
__bp__ = '/file'
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="文件", description="文件管理")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post('/upload')
def upload_file(form: UploadFileForm):
    """上传文件"""
    print(form.file.filename)
    print(form.file_type)
    form.file.save(os.path.join(FILE_PATH, 'test.jpg'))
    return {"code": 0, "message": "ok"}


@api.get('/<filename>')
def download_file(path: DownloadFilePath):
    """下载文件"""
    file = os.path.join(FILE_PATH, path.filename)
    if os.path.exists(file):
        return make_response(send_file(file, as_attachment=True, cache_timeout=60))
    raise FileNotExistException()


@api.get('/image/<filename>')
def get_image(path: DownloadFilePath):
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
