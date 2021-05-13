# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:24
import math

from flask import Blueprint

from sqlalchemy import func


from app.models import db
from app.models.user import User, Role, Permission
from app.utils.exceptions import UserNotExistException, RoleExistException, RoleNotExistException, RoleHasUserException, \
    UserExistException
from app.utils.jwt_tools import super_required, permission, role_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/admin'
api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('/permissions', methods=['GET'])
@permission(name='获取所有权限', module='权限', uuid=__bp__)
@role_required
def get_auths():
    auths = Permission.query.all()
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
@permission(name='新建角色', module='角色', uuid=__bp__)
@role_required
def create_role():
    form = CreateRoleForm().validate_for_api()
    role = Role.query.filter_by(name=form.name.data).first()
    if role:
        raise RoleExistException()
    Role.create(name=form.name.data, describe=form.describe.data, auth_ids=form.auth_ids.data)

    return response(0, 'ok')


@api.route('/roles', methods=['GET'])
@permission(name='获取所有角色', module='角色', uuid=__bp__)
@role_required
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
@permission(name='更新角色', module='角色', uuid=__bp__)
@role_required
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
@permission(name='删除角色', module='角色', uuid=__bp__)
@role_required
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
def add_user():
    form = AddUserForm().validate_for_api()
    user = User.query.filter_by(name=form.name.data).first()
    if user:
        raise UserExistException()
    User.create(form)
    return response(0, 'ok')


@api.route('/users', methods=['GET'])
@permission(name='获取所有用户', module='用户', uuid=__bp__)
@role_required
def get_users():
    form = GetUsersForm().validate_for_api()
    limit = form.page_size.data
    offset = form.page.data * limit
    users = User.query.filter(User.is_super != True).offset(offset).limit(limit).all()
    total = db.session.query(func.count(User.id)).filter(User.is_super != True).scalar()
    total_page = math.ceil(total / limit)
    data = [user.data() for user in users]
    return response(0, 'ok', data=data, total=total, total_page=total_page)


@api.route('/password/<uid>', methods=['PUT'])
@permission(name='修改用户密码', module='用户', uuid=__bp__)
@role_required
def modify_user_password(uid):
    form = ModifyPasswordForm().validate_for_api()

    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise UserNotExistException()

    user.modify_password(new_password=form.password.data, admin=True)
    return response(0, 'ok')


@api.route('/users/<uid>', methods=['DELETE'])
@permission(name='删除用户', module='用户', uuid=__bp__)
@role_required
def delete_user(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise UserNotExistException()
    db.session.delete(user)
    db.session.commit()
    return response(0, 'ok')


@api.route('user/role', methods=['PUT'])
@permission(name='给用户添加角色', module='用户', uuid=__bp__)
@role_required
def set_user_role():
    form = UserRoleForm().validate_for_api()
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        raise UserNotExistException()
    user.roles = Role.query.filter(Role.id.in_(form.role_ids.data)).all()
    db.session.commit()
    return response(0, 'ok')


@api.route('role/auth', methods=['PUT'])
@permission(name='给角色添加权限', module='角色', uuid=__bp__)
@role_required
def set_role_auth():
    form = RoleAuthForm().validate_for_api()
    role = Role.query.filter_by(id=form.role_id.data).first()
    if not role:
        raise RoleNotExistException()
    role.permissions = Permission.query.filter(Permission.id.in_(form.auth_ids.data)).all()
    db.session.commit()
    return response(0, 'ok')
