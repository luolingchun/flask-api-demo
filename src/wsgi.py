# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53
from flask import redirect, url_for
from flask.cli import click, with_appcontext
from flask_migrate import Migrate
from geoalchemy2.alembic_helpers import include_object, render_item, writer
from sqlalchemy import select

from app import create_app
from app.model import db

app = create_app()

# compare_server_default=True,include_object=include_object,render_item=render_item,process_revision_directives=writer
migrate = Migrate(app, db, render_as_batch=False,
                  # configure for geoalchemy2
                  include_object=include_object,
                  render_item=render_item,
                  process_revision_directives=writer)


@app.route("/")
def index():
    """根目录重定向到openapi"""
    return redirect(url_for("openapi.openapi"))


@app.cli.command("test")
@click.argument("a")
@click.option("--b", default="b", help="option help")
def test(a, b):
    """test flask cli command"""
    print(a)
    print(b)


@app.cli.command("init_db")
@with_appcontext
def init_db():
    """初始化数据库"""
    from app.model.user import User, Role
    user = db.session.execute(select(User).where(User.username == "super")).scalar()  # type:ignore
    if user:
        print("超级管理员已存在.")
    else:
        user = User()
        user.username = "super"
        user.password = "123456"
        user.is_super = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        print("添加超级管理员成功.")

    role = db.session.execute(select(Role).where(Role.name == "普通用户")).scalar()  # type:ignore
    if role:
        print("普通用户角色已存在.")
    else:
        role = Role()
        role.name = "普通用户"
        role.describe = "默认权限组"
        db.session.add(role)
        db.session.commit()
        print("添加普通用户角色成功.")


@app.cli.command("register_permission")
@with_appcontext
def register_permission():
    """注册权限"""
    from app.utils.jwt_tools import permissions
    from app.model import db
    from app.model.user import Permission

    for name, module, uuid in permissions:
        permission = db.session.execute(select(Permission).where(Permission.name == name)).scalar()
        if permission:
            print(f"{permission} is exists.")
            continue
        permission = Permission()
        permission.name = name
        permission.module = module
        permission.uuid = uuid
        db.session.add(permission)
        db.session.commit()
        print(f"{name} register success.")


if __name__ == "__main__":
    # app.config["SQLALCHEMY_ECHO"] = True
    app.run("0.0.0.0", 5000, debug=True)
