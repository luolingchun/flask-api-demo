# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/4/23 15:52
from enum import Enum


class PermissionGroup(str, Enum):
    USER = '用户'
    ROLE = '角色'
    BOOK = '图书'
