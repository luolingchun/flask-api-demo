# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic import EmailStr

from app.form import JsonResponse


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=4, max_length=32, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    confirm_password: str = Field(..., min_length=6, description="确认密码")
    email: EmailStr = Field(..., description="邮箱")
    role_ids: Optional[List[int]] = Field([], description="角色ID列表")


class LoginBody(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class PasswordBody(BaseModel):
    old_password: str = Field(..., description="密码")
    new_password: str = Field(..., description="新密码")
    confirm_password: str = Field(..., description="验证密码")


class UserData(BaseModel):
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")


class UserInfoResponse(JsonResponse):
    data: UserData
