# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base, db
from ..utils.exceptions import UserNotExistException, PasswordException, ActiveException
from ..forms.user import RegisterForm

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class User(Base):
    name = db.Column(db.String(24), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(24), unique=True, nullable=True, comment='邮箱')
    is_admin = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment='是否是超级管理员')
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, comment='是否激活')
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    _password = db.Column('password', db.String(100))

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

    def modify_password(self, old_password, new_password):
        if self.check_password(old_password):
            self._password = new_password
            db.session.commit()
            return True
        raise PasswordException(message='原始密码错误')

    @staticmethod
    def get(name):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def create(form: RegisterForm):
        user = User()
        user.name = form.name.data
        user.password = form.password.data
        if form.email.data:
            user.email = form.email.data
        db.session.add(user)
        db.session.commit()

    @classmethod
    def verify(cls, name, password):
        user = cls.query.filter_by(name=name).first()
        if user is None:
            raise UserNotExistException()
        if not user.check_password(password):
            raise PasswordException()
        if not user.is_active:
            raise ActiveException()
        return user


class Role(Base):
    name = db.Column(db.String(24), unique=True, comment='角色名称')
    describe = db.Column(db.String(255), comment='角色描述')

    @staticmethod
    def create(name, describe):
        role = Role()
        role.name = name
        role.describe = describe
        db.session.add(role)
        db.session.commit()

    def data(self):
        return {'id': self.id, 'name': self.name, 'describe': self.describe}
