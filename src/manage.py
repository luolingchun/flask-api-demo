# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:59

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app.models import db
from app.uwsgi import app

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
    print('test')


@manager.command
def init_db():
    from app.models.user import User, Auth, Role
    from app.utils.jwt_tools import auths
    user = db.session.query(User).filter_by(name='super').first()
    if user:
        print('超级管理员已存在.')
    else:
        user = User()
        user.name = 'super'
        user.password = '123456'
        user.is_admin = True
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


manager.add_command("runserver", Server(use_debugger=True, host='0.0.0.0', port='5000'))
# 数据库迁移
# 1. python manage.py db init
# 2. python manage.py db migrate
# 3. python manage.py db upgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
