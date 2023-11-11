# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 17:11
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic import EmailStr

from app.form import JsonResponse


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=4, max_length=32, description="username")
    password: str = Field(..., min_length=6, description="password")
    confirm_password: str = Field(..., min_length=6, description="confirm password")
    email: EmailStr = Field(..., description="email")
    role_ids: Optional[List[int]] = Field([], description="role id")


class LoginBody(BaseModel):
    username: str = Field(..., description="username")
    password: str = Field(..., description="password")


class PasswordBody(BaseModel):
    old_password: str = Field(..., description="old password")
    new_password: str = Field(..., description="new password")
    confirm_password: str = Field(..., description="confirm password")


class UserData(BaseModel):
    username: str = Field(..., description="username")
    email: EmailStr = Field(..., description="email")


class UserInfoResponse(JsonResponse):
    data: UserData
