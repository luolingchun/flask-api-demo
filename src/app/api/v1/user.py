# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05

from flask import request

from app.models.user import User
from app.utils.redprint import Redprint
from app.utils.response import response
from app.validators.forms import UserForm

api = Redprint('users')


@api.route('', methods=['POST'])
def login():
    form = UserForm(data=request.json)
    if form.validate():
        verify = User.verify(
            form.username.data,
            form.password.data,
        )
        if verify:
            return
    else:
        return response(1, form.errors)
    return 'get user'


@api.route('/register', methods=['POST'])
def create_client():
    form = UserForm().validate_for_api()
    User.create(
        form.name.data,
        form.password.data,
    )
    return response(0, 'ok')
