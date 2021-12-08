# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/16 17:27

from functools import wraps

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, create_access_token, \
    create_refresh_token

from app.models import db
from app.models.user import User
from app.utils.exceptions import AuthException, InvalidTokenException, UserNotExistException, ExpiredTokenException

jwt_manager = JWTManager()

# 存放所有权限，数据库初始化时使用
permissions = []


def role_required(name, module, uuid):
    """
    装饰器工厂函数
    :param name: 权限名称
    :param module: 权限模块
    :param uuid: 唯一ID
    :return: decorator
    """

    def decorator(func):
        """装饰器，为func添加权限属性"""
        global permissions
        permissions.append([name, module, uuid])
        setattr(func, 'uuid', uuid)

        @wraps(func)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()
            user = get_current_user()

            if is_user_allowed(user, func.uuid):
                return func(*args, **kwargs)
            else:
                raise AuthException(message='权限不足')

        # 复制全局变量
        wrapper.__extra_globals__ = func.__globals__
        wrapper.__extra_globals__.update(**getattr(func, "__extra_globals__", {}))

        return wrapper

    return decorator


def login_required(func):
    """登录装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)

    # 复制全局变量
    wrapper.__extra_globals__ = func.__globals__
    wrapper.__extra_globals__.update(**getattr(func, "__extra_globals__", {}))

    return wrapper


@jwt_manager.user_lookup_loader
def user_lookup_loader_callback(_, jwt_payload):
    user = db.session.query(User).filter_by(id=jwt_payload['id']).first()
    if user is None:
        return UserNotExistException()
    return user


@jwt_manager.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    """token过期处理"""
    print(jwt_headers and jwt_payload)
    return ExpiredTokenException()


@jwt_manager.invalid_token_loader
def invalid_token_callback(e):
    """无效token处理"""
    print(e)
    return InvalidTokenException()


@jwt_manager.unauthorized_loader
def unauthorized_callback(e):
    print(e)
    return AuthException()


@jwt_manager.additional_claims_loader
def add_claims_to_access_token(identity):
    return identity


def get_token(user):
    identity = {'id': user.id}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


def is_user_allowed(user, uuid):
    """判断用户是否有权限"""
    if user.is_super:
        return True
    roles = user.roles
    uuid_list = [p.uuid for role in roles for p in role.permissions]

    return uuid in uuid_list
