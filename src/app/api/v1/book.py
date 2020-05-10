# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask import Blueprint

from app.utils.redprint import Redprint

api = Redprint('books')


@api.route('')
def get_book():
    return 'get book'
