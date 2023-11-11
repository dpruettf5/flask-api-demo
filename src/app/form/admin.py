# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/17 15:36
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from app.form import JsonResponse, PageModel


class PermissionData(BaseModel):
    id: int = Field(..., description="id")
    name: str = Field(..., description="name")
    module: str = Field(..., description="module")


class PermissionsResponse(JsonResponse):
    data: Optional[Dict[str, List[PermissionData]]]


class UsersQuery(PageModel):
    pass


class RoleData(BaseModel):
    id: int
    name: str = Field(None, description="name")
    describe: str = Field(None, max_length=256, description="description")
    permissions: List[PermissionData]


class UserData(BaseModel):
    id: int
    username: str = Field(None, description="username")
    fullname: str = Field(None, description="full name")
    email: str = Field(None, description="email")
    roles: List[RoleData]


class GetUsersResponse(JsonResponse):
    data: List[UserData]
    total: int = Field(None, description="total")
    total_page: int = Field(None, description="total page")


class UserPath(BaseModel):
    id: int = Field(..., description="id")


class ModifyPasswordBody(BaseModel):
    password: str = Field(..., description="password")
    confirm_password: str = Field(..., description="confirm password")


class CreateRoleBody(BaseModel):
    name: str = Field(..., description="name")
    describe: str = Field(None, max_length=256, description="description")
    permission_ids: Optional[List[int]] = Field([], description="permission ids")


class RolesQuery(PageModel):
    pass


class GetRolesResponse(JsonResponse):
    data: List[RoleData]
    total: int = Field(None, description="total")
    total_page: int = Field(None, description="total page")


class RolePath(BaseModel):
    id: int = Field(..., description="id")


class UpdateRoleBody(BaseModel):
    name: str = Field(None, description="角色名称")
    describe: str = Field(None, max_length=256, description="description")


class UserRoleBody(BaseModel):
    id: int = Field(..., description="用户ID")
    role_ids: Optional[List[int]] = Field([], description="role ids")


class RolePermissionBody(BaseModel):
    id: int = Field(..., description="角色ID")
    permission_ids: Optional[List[int]] = Field([], description="id")
