# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24

r"""
采用经典的权限五表设计：
User        Role        Permission
  \         /   \        /
   \       /     \      /
    uer_role     role_permission
User和Role为多对多关系
Role和Auth为多对多关系
"""

from werkzeug.security import generate_password_hash, check_password_hash

from app.form.user import RegisterBody
from app.utils.exceptions import PasswordException, ActiveException, UserExistException, EmailExistException
from . import Base, db
from ..form.admin import UpdateRoleBody

user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)

role_permission = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)


class User(Base):
    __tablename__ = "user"
    __table_args__ = ({"comment": "用户表"})
    username = db.Column(db.String(32), unique=True, nullable=False, comment="username")
    fullname = db.Column(db.String(32), unique=False, nullable=False, default="", comment="full name")
    email = db.Column(db.String(32), unique=True, nullable=True, comment="email")
    is_super = db.Column(db.Boolean, unique=False, nullable=False, default=False, comment="is super")
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, comment="is active")
    _password = db.Column("password", db.Text, comment="password")

    roles = db.relationship("Role", secondary=user_role, back_populates="users")

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
            raise PasswordException(message="passwords do not match")
        if admin:
            self.password = new_password
            db.session.commit()
            return
        if self.check_password(old_password):
            self.password = new_password
            db.session.commit()
        else:
            raise PasswordException(message="password incorrect")

    @classmethod
    def create(cls, body: RegisterBody):
        cls.verify_register(body)
        user = User()
        user.username = body.username
        user.password = body.password
        user.email = body.email

        # 添加默认角色
        role_ids = body.role_ids if body.role_ids else [1]
        user.roles = db.session.query(Role).filter(Role.id.in_(role_ids)).all()
        db.session.add(user)
        db.session.commit()

    def data(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "is_active": self.is_active,
            "roles": [role.data() for role in self.roles]
        }

    @classmethod
    def verify_register(cls, model: RegisterBody):
        if db.session.query(cls).filter(cls.username == model.username).first():
            raise UserExistException(message="username taken")
        if db.session.query(cls).filter(cls.email == model.email).first():
            raise EmailExistException()
        if model.password != model.confirm_password:
            raise PasswordException(message="passwords do not match")

    @classmethod
    def verify_login(cls, username, password):
        """验证用户名密码"""
        user = db.session.query(cls).filter(cls.username == username).first()
        if user is None:
            raise PasswordException(message="wrong username or password")
        if not user.check_password(password):
            raise PasswordException(message="wrong username or password")
        if not user.is_active:
            raise ActiveException()
        return user


class Role(Base):
    __tablename__ = "role"
    __table_args__ = ({"comment": "role table"})
    name = db.Column(db.String(32), unique=True, comment="role name")
    describe = db.Column(db.String(255), comment="description")

    users = db.relationship("User", secondary=user_role, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permission, back_populates="roles")

    @staticmethod
    def create(name, describe, permission_ids):
        role = Role()
        role.name = name
        role.describe = describe

        if permission_ids:
            role.permissions = db.session.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        db.session.add(role)
        db.session.commit()

    def update(self, body: UpdateRoleBody):
        self.name = body.name
        self.describe = body.describe
        db.session.commit()

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "permissions": [permission.data() for permission in self.permissions]
        }


class Permission(Base):
    __tablename__ = "permission"
    __table_args__ = ({"comment": "permission table"})
    name = db.Column(db.String(32), unique=True, comment="permission name")
    module = db.Column(db.String(32), comment="permissions module")
    uuid = db.Column(db.String(255), unique=True, comment="uuid")

    roles = db.relationship("Role", secondary=role_permission, back_populates="permissions")

    def __repr__(self):
        return f"{self.name}-{self.uuid}"

    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "module": self.module
        }
