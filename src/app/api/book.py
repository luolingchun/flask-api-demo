# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint, request
from spectree import Response

from app.specs import spec, JsonResponse
from app.specs.book import QueryBook, CreateBook, RequestHeader
from app.utils.enums import AuthModule
from app.utils.jwt_tools import role_required, add_auth, login_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/book'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('', methods=['POST'])
@add_auth(name='创建图书', module=AuthModule.BOOK, prefix='1e1cbdb2-6bdb-4091-91ec-5268fa8f2b73')
@role_required
@spec.validate(headers=RequestHeader, json=CreateBook, resp=Response(HTTP_200=JsonResponse), tags=["book"])
def create_book():
    """创建图书"""
    _json = request.json
    print(_json)
    cb = CreateBook(**_json)
    print(cb.name)
    return response(JsonResponse())


@api.route('<int:bid>', methods=['GET'])
@add_auth(name='获取图书', module=AuthModule.BOOK, prefix='0701182b-820b-4a49-bd03-a6c4e17e9120')
@login_required
@spec.validate(query=QueryBook, tags=["book"])
def get_book(bid):
    """查询图书"""
    return f'get book {bid}'


@api.route('<int:id>', methods=['DELETE'])
@add_auth(name='删除图书', module=AuthModule.BOOK, prefix='60362b76-4faf-4245-9bfa-02a063c881d1')
@role_required
@spec.validate(query=QueryBook, tags=["book"])
def delete_book(id):
    """删除图书"""
    return f'delete book {id}'
