# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05

from flask import Blueprint
from flasgger.utils import swag_from

from app.models.user import User
from app.utils.exceptions import UserExistException
from app.utils.jwt import get_token, login_required
from app.utils.response import response
from app.validators.forms import RegisterForm, LoginForm

__version__ = '/v1'
__bp__ = '/user'

api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('/register', methods=['POST'])
@swag_from('api_docs/user/register.yml')
def register():
    form = RegisterForm().validate_for_api()
    user = User.get(name=form.name.data)
    if user:
        raise UserExistException()
    User.create(form)
    return response(0, 'ok')


@api.route('/login', methods=['POST'])
@swag_from('api_docs/user/login.yml')
def login():
    form = LoginForm().validate_for_api()
    user = User.verify(form.name.data, form.password.data)
    access_token = get_token(user)
    return response(0, 'ok', access_token)


@api.route('/info', methods=['GET'])
@login_required
@swag_from('api_docs/user/get_info.yml')
def get_info():
    return 'test'
