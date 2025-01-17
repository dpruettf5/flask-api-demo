# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 16:05
from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag

from app.config import API_PREFIX, JWT, BASIC
from app.form.book import BookBody, BookQuery
from app.utils.enums import PermissionGroup
from app.utils.http_basicauth import basic_required
from app.utils.jwt_tools import role_required
from app.utils.response import response

__version__ = "/v1"
__bp__ = "/book"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="books", description="books management")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag], abp_security=JWT)


@api.post("")
@role_required(name="创建图书", module=PermissionGroup.BOOK, uuid="1e1cbdb2-6bdb-4091-91ec-5268fa8f2b73")
def create_book(body: BookBody):
    """create book"""
    print(body.name)
    print(body.author)
    return response()


@api.get("/<int:id>", security=BASIC)
@basic_required
def get_book(path: BookQuery):
    """get book"""
    print(path)
    return response(data=path.id)


@api.delete("/<int:id>")
def delete_book(path: BookQuery):
    """delete book"""
    print(f"delete {path.id}")
    return response()
