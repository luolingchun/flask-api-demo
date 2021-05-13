# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import API_PREFIX
from app.form.book import CreateBook, QueryBook
from app.utils.enums import PermissionGroup
from app.utils.jwt_tools import permission, role_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/book'
api = APIBlueprint(__bp__, __name__, url_prefix=API_PREFIX + __version__ + __bp__)

tag = Tag(name=__version__ + __bp__, description="图书")


@api.post('', tags=[tag])
@permission(name='创建图书', module=PermissionGroup.BOOK, uuid='1e1cbdb2-6bdb-4091-91ec-5268fa8f2b73')
@role_required
def create_book(json: CreateBook):
    """创建图书"""
    print(json.name)
    print(json.author)
    return response()


@api.get('/<int:bid>', tags=[tag])
def get_book(path: QueryBook):
    """查询图书"""
    print(path)
    return response(data=path.bid)


@api.delete('/<int:bid>', tags=[tag])
def delete_book(path: QueryBook):
    """删除图书"""
    print(f"delete {path.bid}")
    return response()
