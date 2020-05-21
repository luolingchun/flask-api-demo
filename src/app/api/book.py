# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint
from flasgger import swag_from

from app.utils.jwt import role_required, add_auth, login_required

__version__ = '/v1'
__bp__ = '/book'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('<int:id>', methods=['GET'])
@add_auth(name='获取图书', module='图书', prefix=__bp__)
@login_required
@swag_from('api_docs/book/get_book.yml')
def get_book(id):
    return f'get book {id}'


@api.route('<int:id>', methods=['DELETE'])
@add_auth(name='删除图书', module='图书', prefix=__bp__)
@role_required
@swag_from('api_docs/book/delete_book.yml')
def delete_book(id):
    return f'delete book {id}'
