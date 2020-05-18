# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:59

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app.webapp import app
from app.models.base import db

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def test():
    print('test')


@manager.command
def init_db():
    from app.models.user import User, Auth
    from app.utils.jwt import auths
    user = User.query.filter_by(name='super').first()
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
        auth = Auth.query.filter_by(name=name).first()
        if auth:
            continue
        auth = Auth()
        auth.name = name
        auth.module = module
        auth.endpoint = endpoint
        db.session.add(auth)
        db.session.commit()
    print('添加权限成功.')


manager.add_command("runserver", Server(use_debugger=True))
# 数据库迁移
# 1. python manage.py db init
# 2. python manage.py db migrate
# 3. python manage.py db upgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()