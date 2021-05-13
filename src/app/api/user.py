# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_jwt_extended import get_current_user
from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag

from app.config import JWT, API_PREFIX
from app.form.user import RegisterModel, LoginModel, PasswordModel, UserInfo
from app.models import db
from app.models.user import User, Permission
from app.utils.jwt_tools import get_token, login_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/user'

api = APIBlueprint(__bp__, __name__, url_prefix=API_PREFIX + __version__ + __bp__)

tag = Tag(name=__version__ + __bp__, description="用户")


@api.post('/register', tags=[tag])
def register(json: RegisterModel):
    # 用户注册时默认没有角色
    json.role_ids = []
    User.create(json)
    return response()


@api.post('/login', tags=[tag])
def login(json: LoginModel):
    user = User.verify_login(json.username, json.password)
    access_token, refresh_token = get_token(user)
    return response(data={"access_token": access_token, "refresh_token": refresh_token})


@api.get('/info', tags=[tag], responses={"200": UserInfo}, security=JWT)
@login_required
def get_info():
    user = get_current_user()
    data = {
        'username': user.username,
        'email': user.email,
    }
    return response(data=data)


@api.put('/password', tags=[tag], security=JWT)
@login_required
def modify_password(json: PasswordModel):
    user = get_current_user()
    user.modify_password(json.old_password, json.new_password, json.confirm_password)
    return response()


@api.get('/permissions', tags=[tag], security=JWT)
@login_required
def get_permissions():
    user = get_current_user()
    if user.is_super:
        permissions = db.session.query(Permission).all()
    else:
        roles = user.roles
        permissions = [permission for role in roles for permission in role.permissions]
    data = {}
    for permission in permissions:
        permission_data = permission.data()
        module = permission_data['module']
        if not data.get(module):
            data[module] = []
            data[module].append(permission_data)
        else:
            data[module].append(permission_data)
    return response(data=data)
