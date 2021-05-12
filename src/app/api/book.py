# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import API_PREFIX
from app.form.book import CreateBook
from app.utils.enums import PermissionGroup
from app.utils.jwt_tools import role_required, permission
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


@api.get('<int:bid>')
@permission(name='获取图书', module=PermissionGroup.BOOK, uuid='0701182b-820b-4a49-bd03-a6c4e17e9120')
# @login_required
def get_book(bid):
    """查询图书"""
    data = {
        "id": bid,
        "name": "三国",
        "authors": ["罗贯中"]
    }
    print(data)
    return response(data=data)


@api.delete('<int:bid>')
@permission(name='删除图书', module=PermissionGroup.BOOK, uuid='60362b76-4faf-4245-9bfa-02a063c881d1')
# @role_required
def delete_book(bid):
    """删除图书"""
    print(f"delete {bid}")
    return response()
