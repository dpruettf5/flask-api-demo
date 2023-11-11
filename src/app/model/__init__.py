# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:24
import math
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.utils.exceptions import ResourceExistException

db = SQLAlchemy()


def get_offset_limit(page, page_size):
    """gets page number"""
    page = 1 if page < 1 else page
    limit = page_size
    offset = (page - 1) * limit
    return offset, limit


def get_total_page(model, condition, limit):
    """get toal number of pages"""
    total = db.session.query(func.count(model.id)).filter(*condition).scalar()
    total_page = math.ceil(total / limit)
    return total, total_page


def validate_name(model, name, message="name"):
    if db.session.query(model).filter(model.name == name).first():
        raise ResourceExistException(message=f"{message}already exists")


def validate_name_when_update(model, model_id, name, message="name"):
    if db.session.query(model).filter(model.id != model_id, model.name == name).first():
        raise ResourceExistException(message=f"{message}already exists")


class Base(db.Model):
    """Basic database model: provide the ID, creation time, and update time"""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
