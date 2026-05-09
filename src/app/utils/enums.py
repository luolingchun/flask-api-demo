from enum import Enum


class PermissionGroup(str, Enum):
    USER = "用户"
    ROLE = "角色"
    PERMISSION = "权限"
    BOOK = "图书"
    JOB = "任务"
