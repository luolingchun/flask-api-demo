# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base, db

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class User(Base):
    name = db.Column(db.String(24), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(24), unique=True, nullable=True, comment='邮箱')
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment='是否是超级管理员')
    active = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment='是否激活')
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    _password = db.Column('password', db.String(100))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def create(username, password):
        user = User()
        user.name = username
        user.password = password
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def verify(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None

        if not user.check_password(password):
            return None

        return {'uid': user.id}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


class Role(Base):
    name = db.Column(db.String(24), comment='角色名称')
    describe = db.Column(db.String(255), comment='角色描述')
