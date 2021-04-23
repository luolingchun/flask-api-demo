# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05

from flask import Blueprint

from flask_jwt_extended import get_current_user

from app.models.user import User, Auth
from app.utils.exceptions import UserExistException
from app.utils.jwt_tools import get_token, login_required
from app.utils.response import response


__version__ = '/v1'
__bp__ = '/user'

api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('/register', methods=['POST'])
def register():
    form = RegisterForm().validate_for_api()
    user = User.query.filter_by(name=form.name.data).first()
    if user:
        raise UserExistException()
    # 用户中注册时不能自己添加角色
    form.role_ids.data = None
    User.create(form)
    return response(0, 'ok')


@api.route('/login', methods=['POST'])
def login():
    form = LoginForm().validate_for_api()
    user = User.verify(form.name.data, form.password.data)
    access_token = get_token(user)
    return response(0, 'ok', data=access_token)


# @api.route('/info', methods=['GET'])
# @login_required
# def get_info():
#     user = get_current_user()
#     data = {
#         'name': user.name,
#         'email': user.email
#     }
#     return response(0, 'ok', data=data)


@api.route('password', methods=['PUT'])
@login_required
def modify_password():
    form = ModifyPasswordForm().validate_for_api()
    user = get_current_user()
    user.modify_password(form.old_password.data, form.new_password.data)
    return response(0, 'ok')


@api.route('/auths', methods=['GET'])
@login_required
def get_auths():
    current_user = get_current_user()
    if current_user.is_admin:
        auths = Auth.query.all()
    else:
        roles = current_user.roles.all()
        auths = [auth for role in roles for auth in role.auths.all()]
    data = {}
    for auth in auths:
        auth_data = auth.data()
        module = auth_data['module']
        if not data.get(module):
            data[module] = []
            data[module].append(auth_data)
        else:
            data[module].append(auth_data)
    return response(0, 'ok', data=data)
