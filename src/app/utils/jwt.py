# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/16 17:27

from functools import wraps

from flask import request, current_app
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, \
    create_access_token, create_refresh_token

from app.models.user import User, Auth
from app.utils.exceptions import AuthException, InvalidTokenException, UserNotExistException, \
    ExpiredTokenException

jwt = JWTManager()
identity = {
    'uid': -1
}

auths = []


def add_auth(name, module, prefix):
    def wrapper(func):
        auths.append([name, module, prefix + '.' + func.__name__])
        return func

    return wrapper


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
        if not current_user.is_admin:
            roles = current_user.roles.all()
            it = is_user_allowed(roles)
            if not it:
                raise AuthException(message='权限不足')
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


def get_access_token(user, fresh=False, expires_delta=None):
    identity['uid'] = user.id
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


def is_user_allowed(roles):
    endpoints = [auth.endpoint for role in roles for auth in role.auths.all()]
    endpoint = request.endpoint
    return endpoint in endpoints
