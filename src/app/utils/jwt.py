# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/16 17:27

from functools import wraps

from flask import request
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, \
    create_access_token, create_refresh_token

from app.models.user import User
from app.utils.exceptions import AuthException, InvalidTokenException, UserNotExistException, \
    ExpiredTokenException

jwt = JWTManager()
identity = {
    'uid': -1
}


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        if not current_user.is_admin:
            raise AuthException(message='权限不足')
        return fn(*args, **kwargs)

    return wrapper


def role_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        # check current user is active or not
        # 判断当前用户是否为激活状态
        _check_is_active(current_user)
        # not admin
        if not current_user.is_admin:
            group_id = current_user.group_id
            if group_id is None:
                raise AuthFailed(msg='您还不属于任何权限组，请联系超级管理员获得权限')
            from .core import is_user_allowed
            it = is_user_allowed(group_id)
            if not it:
                raise AuthFailed(msg='权限不够，请联系超级管理员获得权限')
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = User.query.filter_by(id=identity['uid']).first()
    if user is None:
        raise UserNotExistException()
    return user


@jwt.expired_token_loader
def expired_loader_callback():
    return ExpiredTokenException()


@jwt.invalid_token_loader
def invalid_loader_callback(e):
    return InvalidTokenException()


@jwt.unauthorized_loader
def unauthorized_loader_callback(e):
    return AuthException()


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'uid': identity['uid'],
    }


def get_token(user):
    identity['uid'] = user.id
    access_token = create_access_token(identity=identity)
    return access_token


def get_access_token(user, scope=None, fresh=False, expires_delta=None, verify_remote_addr=False):
    identity['uid'] = user.id
    identity['scope'] = scope
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    access_token = create_access_token(
        identity=identity,
        fresh=fresh,
        expires_delta=expires_delta,
    )
    return access_token


def get_refresh_token(user, scope=None, expires_delta=None, verify_remote_addr=False):
    identity['uid'] = user.id
    identity['scope'] = scope
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=expires_delta
    )
    return refresh_token
