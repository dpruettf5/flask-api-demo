# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:53
from flask import redirect, url_for
from flask.cli import click, with_appcontext
from flask_migrate import Migrate

# from geoalchemy2.alembic_helpers import include_object, render_item, writer
from app import create_app
from app.model import db

app = create_app()

# compare_server_default=True,include_object=include_object,render_item=render_item,process_revision_directives=writer
migrate = Migrate(app, db, render_as_batch=False)


@app.route("/")
def index():
    """root redire to openapi"""
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
    """init db"""
    from app.model.user import User, Permission, Role
    from app.utils.jwt_tools import permissions
    user = db.session.query(User).filter(User.username == "super").first()
    if user:
        print("super admin exists")
    else:
        user = User()
        user.username = "super"
        user.password = "123456"
        user.is_super = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        print("added super admin")

    for name, module, uuid in permissions:
        permission = db.session.query(Permission).filter_by(name=name).first()
        if permission:
            print(name, module, uuid, "is exists.")
            continue
        permission = Permission()
        permission.name = name
        permission.module = module
        permission.uuid = uuid
        db.session.add(permission)
        db.session.commit()
        print(permission.name, "is success.")
    print("added permission")
    role = db.session.query(Role).filter_by(name="regular user").first()
    if role:
        print("role exists.")
    else:
        role = Role()
        role.name = "regular users"
        role.describe = "default permission group"
        db.session.add(role)
        db.session.commit()
        print("user role added")


@app.cli.command("register_permission")
@with_appcontext
def register_permission():
    ""enrollment permissions"""
    from app.utils.jwt_tools import permissions
    from app.model import db
    from app.model.user import Permission

    for name, module, uuid in permissions:
        permission = db.session.query(Permission).filter(Permission.name == name).first()
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
