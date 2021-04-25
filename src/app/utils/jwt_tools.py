# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/16 17:27

from functools import wraps

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, \
    create_access_token, create_refresh_token

from app.models import db
from app.models.user import User
from app.utils.exceptions import AuthException, InvalidTokenException, UserNotExistException, \
    ExpiredTokenException

jwt_manager = JWTManager()

# 存放所有权限，数据库初始化时使用
auths = []


def add_auth(name, module, uuid):
    """添加权限装饰器"""

    def wrapper(func):
        global auths
        auths.append([name, module, uuid])
        setattr(func, 'uuid', uuid)
        return func

    return wrapper


def super_required(fn):
    """管理权限装饰器"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        if not current_user.is_super:
            raise AuthException(message='权限不足')
        return fn(*args, **kwargs)

    return wrapper


def role_required(fn):
    """角色权限装饰器"""

    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()
        user = get_current_user()

        if not hasattr(fn, 'uuid'):
            setattr(fn, 'uuid', 'xxx')
        if is_user_allowed(user, fn.uuid):
            return fn(*args, **kwargs)
        else:
            raise AuthException(message='权限不足')

    return wrapper


def login_required(fn):
    """登录装饰器"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@jwt_manager.user_lookup_loader
def user_lookup_loader_callback(identity):
    user = db.session.query(User).filter_by(id=identity['uid']).first()
    if user is None:
        raise UserNotExistException()
    return user


@jwt_manager.expired_token_loader
def expired_token_loader_callback():
    """token过期处理"""
    return ExpiredTokenException()


@jwt_manager.invalid_token_loader
def invalid_token_loader_callback(e):
    """无效token处理"""
    print(e)
    return InvalidTokenException()


@jwt_manager.unauthorized_loader
def unauthorized_loader_callback(e):
    print(e)
    return AuthException()


@jwt_manager.additional_claims_loader
def add_claims_to_access_token(identity):
    return identity


def get_token(user):
    identity = {'uid': user.id}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


def is_user_allowed(user, uuid):
    """判断用户是否有权限"""
    if user.is_super:
        return True
    roles = user.roles.all()
    uuid_list = [auth.uuid for role in roles for auth in role.auths.all()]

    return uuid in uuid_list
