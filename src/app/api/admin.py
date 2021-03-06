# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:24
import math

from flask import Blueprint
from flasgger import swag_from
from sqlalchemy import func

from app.forms.admin import GetUsersForm, UserRoleForm, CreateRoleForm, UpdateRoleForm, GetRolesForm, RoleAuthForm, \
    AddUserForm
from app.forms.admin import ModifyPasswordForm
from app.models import db
from app.models.user import User, Role, Auth
from app.utils.exceptions import UserNotExistException, RoleExistException, RoleNotExistException, RoleHasUserException, \
    UserExistException
from app.utils.jwt import admin_required, add_auth, role_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/admin'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('/auths', methods=['GET'])
@add_auth(name='获取所有权限', module='权限', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/get_auths.yml')
def get_auths():
    auths = Auth.query.all()
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


@api.route('/roles', methods=['POST'])
@add_auth(name='新建角色', module='角色', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/create_role.yml')
def create_role():
    form = CreateRoleForm().validate_for_api()
    role = Role.query.filter_by(name=form.name.data).first()
    if role:
        raise RoleExistException()
    Role.create(name=form.name.data, describe=form.describe.data, auth_ids=form.auth_ids.data)

    return response(0, 'ok')


@api.route('/roles', methods=['GET'])
@add_auth(name='获取所有角色', module='角色', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/get_roles.yml')
def get_roles():
    form = GetRolesForm().validate_for_api()
    limit = form.page_size.data
    offset = form.page.data * limit
    roles = Role.query.filter().offset(offset).limit(limit).all()
    total = db.session.query(func.count(Role.id)).filter().scalar()
    total_page = math.ceil(total / limit)
    data = [role.data() for role in roles]
    return response(0, 'ok', data=data, total=total, total_page=total_page)


@api.route('/roles/<rid>', methods=['PUT'])
@add_auth(name='更新角色', module='角色', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/update_role.yml')
def update_role(rid):
    form = UpdateRoleForm().validate_for_api()
    role = Role.query.filter_by(id=rid).first()
    if role is None:
        raise RoleNotExistException()
    if Role.query.filter_by(name=form.name.data).first():
        raise RoleExistException(message='角色名称重复')
    role.name = form.name.data
    role.describe = form.describe.data
    db.session.commit()
    return response(0, 'ok', data=role.data())


@api.route('/roles/<int:rid>', methods=['DELETE'])
@add_auth(name='删除角色', module='角色', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/delete_role.yml')
def delete_role(rid):
    role = Role.query.filter_by(id=rid).first()
    if role is None:
        raise RoleNotExistException()
    if role.users.all():
        raise RoleHasUserException()
    db.session.delete(role)
    db.session.commit()
    return response(0, 'ok')


@api.route('/user', methods=['POST'])
@swag_from('api_docs/admin/add_user.yml')
def add_user():
    form = AddUserForm().validate_for_api()
    user = User.query.filter_by(name=form.name.data).first()
    if user:
        raise UserExistException()
    User.create(form)
    return response(0, 'ok')


@api.route('/users', methods=['GET'])
@add_auth(name='获取所有用户', module='用户', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/get_users.yml')
def get_users():
    form = GetUsersForm().validate_for_api()
    limit = form.page_size.data
    offset = form.page.data * limit
    users = User.query.filter(User.is_admin != True).offset(offset).limit(limit).all()
    total = db.session.query(func.count(User.id)).filter(User.is_admin != True).scalar()
    total_page = math.ceil(total / limit)
    data = [user.data() for user in users]
    return response(0, 'ok', data=data, total=total, total_page=total_page)


@api.route('/password/<uid>', methods=['PUT'])
@add_auth(name='修改用户密码', module='用户', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/modify_user_password.yml')
def modify_user_password(uid):
    form = ModifyPasswordForm().validate_for_api()

    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise UserNotExistException()

    user.modify_password(new_password=form.password.data, admin=True)
    return response(0, 'ok')


@api.route('/users/<uid>', methods=['DELETE'])
@add_auth(name='删除用户', module='用户', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/delete_user.yml')
def delete_user(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise UserNotExistException()
    db.session.delete(user)
    db.session.commit()
    return response(0, 'ok')


@api.route('user/role', methods=['PUT'])
@add_auth(name='给用户添加角色', module='用户', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/set_user_role.yml')
def set_user_role():
    form = UserRoleForm().validate_for_api()
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        raise UserNotExistException()
    user.roles = Role.query.filter(Role.id.in_(form.role_ids.data)).all()
    db.session.commit()
    return response(0, 'ok')


@api.route('role/auth', methods=['PUT'])
@add_auth(name='给角色添加权限', module='角色', prefix=__bp__)
@role_required
@swag_from('api_docs/admin/set_role_auth.yml')
def set_role_auth():
    form = RoleAuthForm().validate_for_api()
    role = Role.query.filter_by(id=form.role_id.data).first()
    if not role:
        raise RoleNotExistException()
    role.auths = Auth.query.filter(Auth.id.in_(form.auth_ids.data)).all()
    db.session.commit()
    return response(0, 'ok')
