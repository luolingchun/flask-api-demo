# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

"""
采用经典的权限五表设计：
User        Role        Auth
  \         /   \        /
   \       /     \      /
    uer_role     role_auth
User和Role为多对多关系
Role和Auth为多对多关系
"""

from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base, db
from app.utils.exceptions import UserNotExistException, PasswordException

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_auth = db.Table(
    'role_auth',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('auth_id', db.Integer, db.ForeignKey('auth.id'), primary_key=True)
)


class User(Base):
    name = db.Column(db.String(32), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(32), unique=True, nullable=True, comment='邮箱')
    is_admin = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment='是否是超级管理员')
    # is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, comment='是否激活')
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    _password = db.Column('password', db.String(100), comment='密码')

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

    def modify_password(self, old_password=None, new_password=None, admin=False):
        if admin:
            self.password = new_password
            db.session.commit()
            return True
        if self.check_password(old_password):
            self.password = new_password
            db.session.commit()
            return True
        raise PasswordException(message='原始密码错误')

    @staticmethod
    def create(form):
        user = User()
        user.name = form.name.data
        user.password = form.password.data
        if form.email.data:
            user.email = form.email.data
        # 添加默认角色
        role_ids = form.role_ids.data if form.role_ids.data else [1]
        user.roles = Role.query.filter(Role.id.in_(role_ids)).all()
        db.session.add(user)
        db.session.commit()

    def data(self):
        return {'id': self.id, 'name': self.name, 'email': self.email,
                'roles': [role.data() for role in self.roles.all()]}

    @classmethod
    def verify(cls, name, password):
        user = cls.query.filter_by(name=name).first()
        if user is None:
            raise UserNotExistException()
        if not user.check_password(password):
            raise PasswordException()
        # if not user.is_active:
        #     raise ActiveException()
        return user


class Role(Base):
    name = db.Column(db.String(32), unique=True, comment='角色名称')
    describe = db.Column(db.String(255), comment='角色描述')
    auths = db.relationship('Auth', secondary=role_auth, backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')

    @staticmethod
    def create(name, describe, auth_ids):
        role = Role()
        role.name = name
        role.describe = describe
        if auth_ids:
            role.auths = Auth.query.filter(Auth.id.in_(auth_ids)).all()
        db.session.add(role)
        db.session.commit()

    def data(self):
        return {'id': self.id, 'name': self.name, 'describe': self.describe}


class Auth(Base):
    name = db.Column(db.String(32), unique=True, comment='权限名称')
    module = db.Column(db.String(32), comment='权限模块')
    endpoint = db.Column(db.String(255), comment='路由端点')

    def data(self):
        return {'id': self.id, 'name': self.name, 'module': self.module}
