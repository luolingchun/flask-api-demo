# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_jwt_extended import get_current_user, verify_jwt_in_request, get_jwt_identity, create_access_token
from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag

from app.config import JWT, API_PREFIX
from app.form.user import RegisterBody, LoginBody, PasswordBody, UserInfoResponse
from app.model import db
from app.model.user import User, Permission
from app.utils.exceptions import RefreshException, UserNotExistException
from app.utils.jwt_tools import get_token, login_required
from app.utils.response import response

__version__ = "/v1"
__bp__ = "/user"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="用户", description="用户注册、登录、个人管理")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag], abp_security=JWT)


@api.post("/register")
def register(body: RegisterBody):
    """用户注册"""
    # 用户注册时默认没有角色
    body.role_ids = []
    User.create(body)
    return response()


@api.post("/login")
def login(body: LoginBody):
    """用户登录"""
    user = User.verify_login(body.username, body.password)
    access_token, refresh_token = get_token(user)
    return response(data={"access_token": access_token, "refresh_token": refresh_token})


@api.get("/info", responses={"200": UserInfoResponse})
@login_required
def get_info():
    """获取用户信息"""
    user = get_current_user()
    data = {
        "username": user.username,
        "email": user.email,
    }
    return response(data=data)


@api.put("/password")
@login_required
def modify_password(body: PasswordBody):
    """修改密码"""
    user = get_current_user()
    user.modify_password(body.old_password, body.new_password, body.confirm_password)
    return response()


@api.get("/permissions")
@login_required
def get_permissions():
    """获取用户权限"""
    user = get_current_user()
    if user.is_super:
        permissions = db.session.query(Permission).all()
    else:
        roles = user.roles
        permissions = [permission for role in roles for permission in role.permissions]
    data = {}
    for permission in permissions:
        permission_data = permission.data()
        module = permission_data["module"]
        if not data.get(module):
            data[module] = []
            data[module].append(permission_data)
        else:
            data[module].append(permission_data)
    return response(data=data)


@api.get("/refresh")
def refresh():
    """更新令牌"""
    try:
        verify_jwt_in_request(refresh=True)
    except Exception as e:
        print(e)
        return RefreshException(message="更新令牌失败，请重新登录")

    identity = get_jwt_identity()
    if identity:
        uid = identity["id"]
        user = db.session.query(User).filter_by(id=uid).first()
        if user is None:
            raise UserNotExistException()
        access_token = create_access_token(identity=identity)
    else:
        raise UserNotExistException()
    return response(access_token=access_token)
