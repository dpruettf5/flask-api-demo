# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/5 18:54
"""
global exception handling
"""
import json

from werkzeug.exceptions import HTTPException


class BaseAPIException(HTTPException):
    code = 200
    error_code = -1
    message = "server unknown error"

    def __init__(self, code=None, message=None, error_code=None, headers=None):
        if code:
            self.code = code
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if headers is not None:
            headers_merged = headers.copy()
            headers_merged.update(headers)
            self.headers = headers_merged

        super(BaseAPIException, self).__init__(message, None)

    def get_body(self, *args, **kwargs):
        body = {
            "code": self.error_code,
            "message": self.message,
        }
        text = json.dumps(body, ensure_ascii=False)
        return text

    def get_headers(self, *args, **kwargs):
        return [("Content-Type", "application/json")]


class UnknownException(BaseAPIException):
    code = 500


class ContentTypeException(BaseAPIException):
    error_code = -2
    message = "unsupported content-type"


class ParameterException(BaseAPIException):
    error_code = 1002
    message = "incorrect parameter"


class UserExistException(BaseAPIException):
    error_code = 2001
    message = "user already exists"


class UserNotExistException(BaseAPIException):
    error_code = 2002
    message = "user does not exist"


class PasswordException(BaseAPIException):
    error_code = 2003
    message = "wrong username or password"


class ActiveException(BaseAPIException):
    error_code = 2004
    message = "user is not activated"


class AuthException(BaseAPIException):
    error_code = 2005
    message = "auth failed, no token"


class InvalidTokenException(BaseAPIException):
    error_code = 2006
    message = "bad token"


class InvalidAccessTokenException(BaseAPIException):
    error_code = 20061
    message = "token is incorrect"


class ExpiredTokenException(BaseAPIException):
    error_code = 2007
    message = "token expired"


class EmailExistException(BaseAPIException):
    error_code = 2008
    message = "email is already registered"


class RefreshException(BaseAPIException):
    error_code = 2010
    message = "failed to update token"


class RoleExistException(BaseAPIException):
    error_code = 3001
    message = "role already exists"


class RoleNotExistException(BaseAPIException):
    error_code = 3002
    message = "role does not exist"


class RoleHasUserException(BaseAPIException):
    error_code = 3003
    message = "users are in role and cannot be deleted"


class ResourceNotExistException(BaseAPIException):
    error_code = 4001
    message = "resource does not exist"


class ResourceExistException(BaseAPIException):
    error_code = 4002
    message = "resource exists"


class ResourceConstraintException(BaseAPIException):
    error_code = 4003
    message = "resource is referenced and cannot be deleted"



class JobNotExistException(BaseAPIException):
    error_code = 5001
    message = "task does not exist"


class JobNotRetryException(BaseAPIException):
    error_code = 5002
    message = "retry failed task"


class JobTypeErrorException(BaseAPIException):
    error_code = 5003
    message = "task type is invalid"


class OneClickErrorException(BaseAPIException):
    error_code = 5004
    message = "click exception"


