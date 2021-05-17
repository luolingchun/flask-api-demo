# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

"""
采用经典的权限五表设计：
User        Role        Permission
  \         /   \        /
   \       /     \      /
    uer_role     role_permission
User和Role为多对多关系
Role和Auth为多对多关系
"""

from werkzeug.security import generate_password_hash, check_password_hash

from app.form.user import RegisterModel
from app.utils.exceptions import PasswordException, ActiveException, UserExistException, EmailExistException
from . import Base, db

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)


class User(Base):
    username = db.Column(db.String(32), unique=True, nullable=False, comment='用户名')
    fullname = db.Column(db.String(32), unique=False, nullable=False, default='', comment='姓名')
    email = db.Column(db.String(32), unique=True, nullable=True, comment='邮箱')
    is_super = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment='是否是超级管理员')
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, comment='是否激活')
    _password = db.Column('password', db.Text, comment='密码')

    roles = db.relationship('Role', secondary=user_role, back_populates="users")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

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
            raise PasswordException(message='原始密码错误')

    @classmethod
    def create(cls, model: RegisterModel):
        cls.verify_register(model)
        user = User()
        user.username = model.username
        user.password = model.password
        user.email = model.email

        # 添加默认角色
        role_ids = model.role_ids if model.role_ids else [1]
        user.roles = Role.query.filter(Role.id.in_(role_ids)).all()
        db.session.add(user)
        db.session.commit()

    def data(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email,
            'is_active': self.is_active,
            'roles': [role.data() for role in self.roles]
        }

    @classmethod
    def verify_register(cls, model: RegisterModel):
        if db.session.query(cls).filter(cls.username == model.username).first():
            raise UserExistException(message="用户名不可用")
        if db.session.query(cls).filter(cls.email == model.email).first():
            raise EmailExistException()
        if model.password != model.confirm_password:
            raise PasswordException(message="密码不一致")

    @classmethod
    def verify_login(cls, username, password):
        """验证用户名密码"""
        user = db.session.query(cls).filter(cls.username == username).first()
        if user is None:
            raise PasswordException(message="用户名或密码错误")
        if not user.check_password(password):
            raise PasswordException(message="用户名或密码错误")
        if not user.is_active:
            raise ActiveException()
        return user


class Role(Base):
    name = db.Column(db.String(32), unique=True, comment='角色名称')
    describe = db.Column(db.String(255), comment='角色描述')

    users = db.relationship('User', secondary=user_role, back_populates="roles")
    permissions = db.relationship('Permission', secondary=role_permission, back_populates="roles")

    @staticmethod
    def create(name, describe, permission_ids):
        role = Role()
        role.name = name
        role.describe = describe

        if permission_ids:
            role.permissions = db.session.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        db.session.add(role)
        db.session.commit()

    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'describe': self.describe,
            'permissions': [permission.data() for permission in self.permissions]
        }


class Permission(Base):
    name = db.Column(db.String(32), unique=True, comment='权限名称')
    module = db.Column(db.String(32), comment='权限模块')
    uuid = db.Column(db.String(255), unique=True, comment='权限uuid')

    roles = db.relationship('Role', secondary=role_permission, back_populates="permissions")

    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'module': self.module
        }
