# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:24

from flask_openapi3 import APIBlueprint
from flask_openapi3.models import Tag
from sqlalchemy import and_

from app.config import API_PREFIX, JWT
from app.form.admin import PermissionsResponse, UsersQuery, GetUsersResponse, ModifyPasswordBody, \
    UserPath, CreateRoleBody, RolesQuery, GetRolesResponse, RolePath, UpdateRoleBody, UserRoleBody, \
    RolePermissionBody
from app.form.user import RegisterBody
from app.models import db, get_offset_limit, get_total_page
from app.models.user import User, Permission, Role
from app.utils.enums import PermissionGroup
from app.utils.exceptions import UserExistException, UserNotExistException, RoleExistException, RoleNotExistException, \
    RoleHasUserException
from app.utils.jwt_tools import permission, role_required
from app.utils.response import response

__version__ = '/v1'
__bp__ = '/admin'
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="管理员", description="管理用户、角色、权限")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag], abp_security=JWT)


@api.get('/permissions', responses={"200": PermissionsResponse})
@permission(name='获取所有权限', module=PermissionGroup.PERMISSION, uuid='913aa468-634d-42d4-8a75-6d0ed16723fb')
@role_required
def get_permissions():
    """获取所有权限"""
    permissions = db.session.query(Permission).all()
    data = {}
    for p in permissions:
        p_data = p.data()
        module = p_data['module']
        if not data.get(module):
            data[module] = []
            data[module].append(p_data)
        else:
            data[module].append(p_data)

    return response(data=data)


@api.post('/users')
@permission(name='添加用户', module=PermissionGroup.USER, uuid='82f206e8-a172-4e37-adfd-0a39e8a9fb8e')
@role_required
def add_user(body: RegisterBody):
    """添加用户"""
    user = db.session.query(User).filter(User.username == body.username).first()
    if user:
        raise UserExistException()
    User.create(body)
    return response()


@api.get('/users', responses={"200": GetUsersResponse})
@permission(name='获取所有用户', module=PermissionGroup.USER, uuid='ad62bda9-b1fb-4229-8b49-1f7acc6cadbc')
@role_required
def get_users(query: UsersQuery):
    """获取所有用户"""
    offset, limit = get_offset_limit(query.page, query.page_size)
    condition = [User.is_super != True]
    users = db.session.query(User).filter(*condition).offset(offset).limit(limit).all()
    total, total_page = get_total_page(User, condition, limit)
    data = [user.data() for user in users]
    return response(data=data, total=total, total_page=total_page)


@api.put('/password/<uid>')
@permission(name='修改用户密码', module=PermissionGroup.USER, uuid='4f0d0f12-b552-41dc-8db3-fde11fdb2405')
@role_required
def modify_user_password(path: UserPath, body: ModifyPasswordBody):
    """修改用户密码"""
    user = db.session.query(User).filter(and_(User.id == path.uid, User.is_super != True)).first()
    if user is None:
        raise UserNotExistException()

    user.modify_password(new_password=body.password, confirm_password=body.confirm_password, admin=True)
    return response()


@api.delete('/users/<uid>')
@permission(name="删除用户", module=PermissionGroup.USER, uuid='6502e822-f3da-4d42-a6de-65321b455178')
@role_required
def delete_user(path: UserPath):
    """删除用户"""
    user = db.session.query(User).filter(and_(User.id == path.uid, User.is_super != True)).first()
    if user is None:
        raise UserNotExistException()
    db.session.delete(user)
    db.session.commit()
    return response()


@api.post('/roles')
@permission(name="新建角色", module=PermissionGroup.ROLE, uuid='4b3ba348-e860-41b6-9d97-fd290e713e76')
@role_required
def create_role(body: CreateRoleBody):
    """新建角色"""
    role = db.session.query(Role).filter(Role.name == body.name).first()
    if role:
        raise RoleExistException()
    Role.create(name=body.name, describe=body.describe, permission_ids=body.permission_ids)

    return response()


@api.get('/roles', responses={"200": GetRolesResponse})
@permission(name='获取所有角色', module=PermissionGroup.ROLE, uuid='8abf94aa-b94a-465a-a67b-2e8acba9c59a')
@role_required
def get_roles(query: RolesQuery):
    """获取所有角色"""
    offset, limit = get_offset_limit(query.page, query.page_size)
    roles = db.session.query(Role).offset(offset).limit(limit).all()
    total, total_page = get_total_page(User, [], limit)
    data = [role.data() for role in roles]
    return response(data=data, total=total, total_page=total_page)


@api.put('/roles/<rid>')
@permission(name='更新角色', module=PermissionGroup.ROLE, uuid='cd0de18c-2147-41b6-88f8-023cef35640d')
@role_required
def update_role(path: RolePath, body: UpdateRoleBody):
    """更新角色"""
    role = db.session.query(Role).filter(Role.id == path.rid).first()
    if role is None:
        raise RoleNotExistException()
    if db.session.query(Role).filter(Role.name == body.name).first():
        raise RoleExistException(message='角色名称重复')
    role.name = body.name
    role.describe = body.describe
    db.session.commit()
    return response()


@api.delete('/roles/<int:rid>')
@permission(name='删除角色', module='角色', uuid='cdb35c5d-f5c9-4ff5-ba6c-5bba8349a176')
@role_required
def delete_role(path: RolePath):
    """删除角色"""
    role = db.session.query(Role).filter(Role.id == path.rid).first()
    if role is None:
        raise RoleNotExistException()
    if role.users:
        raise RoleHasUserException()
    db.session.delete(role)
    db.session.commit()
    return response()


@api.put('users/roles')
@permission(name='给用户添加角色', module=PermissionGroup.USER, uuid='a6e4d9c4-6a8c-4095-a4a9-49d7ab2d8790')
@role_required
def set_user_role(body: UserRoleBody):
    """给用户添加角色"""
    user = db.session.query(User).filter(and_(User.id == body.uid, User.is_super != True)).first()
    if user is None:
        raise UserNotExistException()
    user.roles = db.session.query(Role).filter(Role.id.in_(body.role_ids)).all()
    db.session.commit()
    return response()


@api.put('roles/permissions')
@permission(name='给角色添加权限', module=PermissionGroup.ROLE, uuid='376f7d69-cd14-41c2-a4d2-ebdd4ca238bc')
@role_required
def set_role_permission(body: RolePermissionBody):
    """给角色添加权限"""
    role = db.session.query(Role).filter(Role.id == body.rid).first()
    if role is None:
        raise RoleNotExistException()
    role.permissions = db.session.query(Permission).filter(Permission.id.in_(body.permission_ids)).all()
    db.session.commit()
    return response()
