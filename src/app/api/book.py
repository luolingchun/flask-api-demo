# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint, request
from spectree import Response, Tag

from app.specs import spec, JsonResponse
from app.specs.book import QueryBook, CreateBook, QueryBookResponse
from app.utils.enums import AuthModule
from app.utils.jwt_tools import role_required, add_auth
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/book'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)

book_tag = Tag(name='book', description='图书')


@api.route('', methods=['POST'])
@add_auth(name='创建图书', module=AuthModule.BOOK, uuid='1e1cbdb2-6bdb-4091-91ec-5268fa8f2b73')
@role_required
@spec.validate(json=CreateBook, resp=Response(HTTP_200=JsonResponse), tags=[book_tag])
def create_book():
    """创建图书"""
    cb = CreateBook.parse_obj(request.get_json(silent=True))
    print(cb.name)
    return response()


@api.route('<int:bid>', methods=['GET'])
@add_auth(name='获取图书', module=AuthModule.BOOK, uuid='0701182b-820b-4a49-bd03-a6c4e17e9120')
# @login_required
@spec.validate(query=QueryBook, resp=Response(HTTP_200=QueryBookResponse), tags=[book_tag])
def get_book(bid):
    """查询图书"""
    data = {
        "id": bid,
        "name": "三国",
        "authors": ["罗贯中"]
    }
    print(data)
    return response(data=data)


@api.route('<int:bid>', methods=['DELETE'])
@add_auth(name='删除图书', module=AuthModule.BOOK, uuid='60362b76-4faf-4245-9bfa-02a063c881d1')
# @role_required
@spec.validate(resp=Response(HTTP_200=JsonResponse), tags=[book_tag])
def delete_book(bid):
    """删除图书"""
    print(f"delete {bid}")
    return response()
