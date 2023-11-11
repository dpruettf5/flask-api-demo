# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11
from flask_openapi3 import FileStorage
from pydantic import BaseModel, Field


class PageModel(BaseModel):
    page: int = Field(1, ge=1, description="page")
    page_size: int = Field(15, ge=1, description="page size")


class IdModel(BaseModel):
    id: int = Field(..., description="id")


class IdStringModel(BaseModel):
    id: str = Field(..., description="id")


class FileModel(BaseModel):
    file: FileStorage


class JsonResponse(BaseModel):
    code: int = Field(default=0, description="code")
    message: str = Field(default="ok", description="message")
