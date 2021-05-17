# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:36
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from app.form import JsonResponse, PageModel


class PermissionData(BaseModel):
    id: int = Field(..., description="ID")
    name: str = Field(..., description="名称")
    module: str = Field(..., description="模块")


class PermissionsResponse(JsonResponse):
    data: Optional[Dict[str, List[PermissionData]]]


class GetUsersModel(PageModel):
    pass


class RoleData(BaseModel):
    id: int
    name: str = Field(None, description="角色名称")
    describe: str = Field(None, description="角色描述")
    permissions: List[PermissionData]


class UserData(BaseModel):
    id: int
    username: str = Field(None, description="用户名")
    fullname: str = Field(None, description="姓名")
    email: str = Field(None, description="邮箱")
    roles: List[RoleData]


class GetUsersResponse(JsonResponse):
    data: List[UserData]
    total: int = Field(None, description="总个数")
    total_page: int = Field(None, description="总页数")


class UserPathModel(BaseModel):
    uid: int = Field(..., description="用户ID")


class ModifyPasswordModel(BaseModel):
    password: str = Field(..., description="密码")
    confirm_password: str = Field(..., description="验证密码")


class CreateRoleModel(BaseModel):
    name: str = Field(..., description="角色名称")
    describe: str = Field(None, description="角色描述")
    permission_ids: Optional[List[int]] = Field([], description="权限ID列表")


class GetRolesModel(PageModel):
    pass


class GetRolesResponse(JsonResponse):
    data: List[RoleData]
    total: int = Field(None, description="总个数")
    total_page: int = Field(None, description="总页数")


class RolePathModel(BaseModel):
    rid: int = Field(..., description="角色ID")


class UpdateRoleModel(BaseModel):
    name: str = Field(None, description="角色名称")
    describe: str = Field(None, description="角色描述")


class UserRoleModel(BaseModel):
    uid: int = Field(..., description="用户ID")
    role_ids: Optional[List[int]] = Field([], description="角色ID列表")


class RolePermissionModel(BaseModel):
    rid: int = Field(..., description="角色ID")
    permission_ids: Optional[List[int]] = Field([], description="权限ID列表")
