# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import API_PREFIX
from app.form.book import BookBody, BookQuery
from app.utils.enums import PermissionGroup
from app.utils.jwt_tools import permission, role_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/book'
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="图书", description="图书管理")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post('')
@role_required
@permission(name='创建图书', module=PermissionGroup.BOOK, uuid='1e1cbdb2-6bdb-4091-91ec-5268fa8f2b73')
def create_book(body: BookBody):
    """创建图书"""
    print(body.name)
    print(body.author)
    return response()


@api.get('/<int:bid>')
def get_book(path: BookQuery):
    """查询图书"""
    print(path)
    return response(data=path.bid)


@api.delete('/<int:bid>')
def delete_book(path: BookQuery):
    """删除图书"""
    print(f"delete {path.bid}")
    return response()
