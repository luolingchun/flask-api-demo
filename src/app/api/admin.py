# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:24

from flask import Blueprint
from app.forms.admin import GetUsersForm, UserRoleForm, CreateRoleForm, UpdateRoleForm
from app.models.base import db
from app.models.user import User, Role
from app.utils.exceptions import UserNotExistException, RoleExistException, RoleNotExistException, RoleHasUserException
from app.utils.jwt import admin_required

__version__ = '/v1'
__bp__ = '/admin'

from app.utils.response import response

api = Blueprint(__bp__, __name__, url_prefix=__version__ + __bp__)


@api.route('/roles', methods=['POST'])
def create_role():
    form = CreateRoleForm().validate_for_api()
    role = Role.query.filter_by(name=form.name.data).first()
    if role:
        raise RoleExistException()
    Role.create(name=form.name.data, describe=form.describe.data)

    # for auth in form.auths.data:
    #     meta = find_auth_module(auth)
    #     if meta:
    #         manager.auth_model.create(auth=meta.auth, module=meta.module, group_id=group.id)

    return response(0, 'ok')


@api.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    if roles is None:
        raise RoleExistException()

    return response(0, 'ok', [role.data() for role in roles])


@api.route('/roles/<int:rid>', methods=['PUT'])
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
    return response(0, 'ok', role.data())


@api.route('/roles/<int:rid>', methods=['DELETE'])
def delete_role(rid):
    role = Role.query.filter_by(id=rid).first()
    if role is None:
        raise RoleNotExistException()
    if role.users.all():
        raise RoleHasUserException()
    db.session.delete(role)
    db.session.commit()
    return response(0, 'ok')


@api.route('/users', methods=['GET'])
# @admin_required
def get_users():
    form = GetUsersForm().validate_for_api()
    print(form.page.data, form.page_size.data, form.role_id.data)
    return


@api.route('/users/<int:uid>', methods=['DELETE'])
@admin_required
def delete_user(uid):
    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise UserNotExistException()
    db.session.delete(user)
    db.session.commit()
    return response(0, 'ok')


@api.route('user/role', methods=['PUT'])
def set_user_role():
    form = UserRoleForm().validate_for_api()
    user = User.query.filter_by(id=form.user_id.data).first()
    if not user:
        raise UserNotExistException()
    user.roles = Role.query.filter(Role.id.in_(form.role_ids.data)).all()
    db.session.commit()
    return response(0, 'ok')
