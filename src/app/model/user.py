# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

r"""
采用经典的权限五表设计：
User        Role        Permission
  \         /   \        /
   \       /     \      /
    uer_role     role_permission
User和Role为多对多关系
Role和Permission为多对多关系
"""
from sqlalchemy import select, String, Boolean, Text, Column, Table, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.form.admin import UpdateRoleBody
from app.form.user import RegisterBody
from app.model import Base, db
from app.utils.exceptions import PasswordException, ActiveException, UserExistException, EmailExistException

UserRole = Table(
    "user_role",
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id"))
)

RolePermission = Table(
    "role_permission",
    db.metadata,
    Column("role_id", Integer, ForeignKey("role.id")),
    Column("permission_id", Integer, ForeignKey("permission.id"))
)


class User(Base):
    __tablename__ = "user"
    __table_args__ = ({"comment": "用户表"})
    username = Column(String(32), unique=True, nullable=False, comment="用户名")
    fullname = Column(String(32), unique=False, nullable=False, default="", comment="姓名")
    email = Column(String(32), unique=True, nullable=True, comment="邮箱")
    is_super = Column(Boolean, unique=False, nullable=False, default=False, comment="是否是超级管理员")
    is_active = Column(Boolean, unique=False, nullable=False, default=True, comment="是否激活")
    _password = Column("password", Text, comment="密码")

    roles: Mapped[list["Role"]] = relationship("Role", secondary=UserRole, back_populates="users")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password: str = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def modify_password(self, old_password=None, new_password=None, confirm_password=None, admin=False):
        if new_password != confirm_password:
            raise PasswordException(message="密码不一致")
        if admin:
            self.password = new_password
            db.session.commit()
            return
        if self.check_password(old_password):
            self.password = new_password
            db.session.commit()
        else:
            raise PasswordException(message="原始密码错误")

    @staticmethod
    def create(body: RegisterBody):
        User.verify_register(body)
        user = User()
        user.username = body.username
        user.password = body.password
        user.email = body.email

        # 添加默认角色
        role_ids = body.role_ids if body.role_ids else [1]
        user.roles = db.session.execute(select(Role).where(Role.id.in_(role_ids))).scalars().all()
        db.session.add(user)
        db.session.commit()

    def data(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "is_active": self.is_active,
            "roles": [role.data() for role in self.roles]
        }

    @classmethod
    def verify_register(cls, body: RegisterBody):
        if db.session.execute(select(cls).where(cls.username == body.username)).scalar():  # type: ignore
            raise UserExistException(message="用户名不可用")
        if db.session.execute(select(cls).where(cls.email == body.email)).scalar():  # type: ignore
            raise EmailExistException()
        if body.password != body.confirm_password:
            raise PasswordException(message="密码不一致")

    @staticmethod
    def verify_login(username, password):
        """验证用户名密码"""
        user = db.session.execute(select(User).where(User.username == username)).scalar()
        if user is None:
            raise PasswordException(message="用户名或密码错误")
        if not user.check_password(password):
            raise PasswordException(message="用户名或密码错误")
        if not user.is_active:
            raise ActiveException()
        return user


class Role(Base):
    __tablename__ = "role"
    __table_args__ = ({"comment": "角色表"})
    name = Column(String(32), unique=True, comment="角色名称")
    describe = Column(String(255), comment="角色描述")

    users: Mapped[list["User"]] = relationship("User", secondary=UserRole, back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary=RolePermission,
                                                           back_populates="roles")

    @staticmethod
    def create(name, describe, permission_ids):
        role = Role()
        role.name = name
        role.describe = describe

        if permission_ids:
            role.permissions = db.session.execute(
                select(Permission).where(Permission.id.in_(permission_ids))
            ).scalars().all()
        db.session.add(role)
        db.session.commit()

    def update(self, body: UpdateRoleBody):
        self.name = body.name
        self.describe = body.describe
        db.session.commit()

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "permissions": [permission.data() for permission in self.permissions]
        }


class Permission(Base):
    __tablename__ = "permission"
    __table_args__ = ({"comment": "权限表"})
    name = Column(String(32), unique=True, comment="权限名称")
    module = Column(String(32), comment="权限模块")
    uuid = Column(String(255), unique=True, comment="权限uuid")

    roles = relationship("Role", secondary=RolePermission, back_populates="permissions")

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "module": self.module
        }
