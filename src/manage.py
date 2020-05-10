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


manager.add_command("runserver", Server(use_debugger=True))
# 数据库迁移
# 1. python manage.py db init
# 2. python manage.py db migrate
# 3. python manage.py db upgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
