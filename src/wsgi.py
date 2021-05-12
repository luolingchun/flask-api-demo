# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53
import sys

sys.path.insert(0, r"D:\workspace\flask-openapi3")
print(sys.path)
from flask.cli import with_appcontext

from app import create_app
from app.models import db

app = create_app()


@app.cli.command("test")
def test():
    """test flask cli command"""
    print('test')


@app.cli.command("init_db")
@with_appcontext
def init_db():
    """初始化数据库"""
    from app.models.user import User, Auth, Role
    from app.utils.jwt_tools import auths
    user = db.session.query(User).filter_by(name='super').first()
    if user:
        print('超级管理员已存在.')
    else:
        user = User()
        user.name = 'super'
        user.password = '123456'
        user.is_super = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        print('添加超级管理员成功.')

    for name, module, endpoint in auths:
        auth = db.session.query(Auth).filter_by(name=name).first()
        if auth:
            continue
        auth = Auth()
        auth.name = name
        auth.module = module
        auth.endpoint = endpoint
        db.session.add(auth)
        db.session.commit()
    print('添加权限成功.')
    role = db.session.query(Role).filter_by(name='普通用户').first()
    if role:
        print('普通用户角色已存在.')
    else:
        role = Role()
        role.name = '普通用户'
        role.describe = '默认权限组'
        db.session.add(role)
        db.session.commit()
    print('添加普通用户角色成功.')
