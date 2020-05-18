# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint

from app.utils.jwt import role_required, add_auth

__version__ = '/v1'
__bp__ = '/book'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('<int:id>', methods=['GET'])
@add_auth(name='获取图书', module='图书', prefix=__bp__)
@role_required
def get_book(id):
    return f'get book {id}'


@api.route('<int:id>', methods=['DELETE'])
@add_auth(name='删除图书', module='图书', prefix=__bp__)
@role_required
def delete_book(id):
    return f'delete book {id}'
