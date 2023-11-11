# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/5/4 15:52
import importlib
import os
import re
import traceback

from flask_cors import CORS
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix


def init_exception(app: OpenAPI):
    from app.utils.exceptions import BaseAPIException, UnknownException

    @app.errorhandler(Exception)
    def handler(e):
        """handle exceptions"""
        if isinstance(e, BaseAPIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            message = e.description
            return BaseAPIException(code, message)
        else:
            print(traceback.format_exc())
            return UnknownException()


def auto_register_api(app: OpenAPI):
    """register blueprint
    """
    here = os.path.dirname(__file__)
    api_dir = os.path.join(here, "api")
    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file == "__init__.py":
                continue
            if not file.endswith(".py"):
                continue
            api_file = os.path.join(root, file)
            rule = re.split(r"src|.py", api_file)[1]
            api_route = ".".join(rule.split(os.sep)).strip(".")
            # noinspection PyBroadException
            try:
                api = importlib.import_module(api_route)
                app.register_api(api.api)
            except AttributeError:
                print(f"module {api_route} auto-enrollment")
            except:
                traceback.print_exc()
                print(f"module {api_route} auto-enrollment")


def register_apis(app: OpenAPI):
    """register the api"""
    # from app.api.user import api as user_api
    # from app.api.admin import api as admin_api
    # from app.api.book import api as book_api
    # from app.api.file import api as file_api
    # from app.api.job import api as job_api
    # app.register_api(user_api)
    # app.register_api(admin_api)
    # app.register_api(book_api)
    # app.register_api(file_api)
    # app.register_api(job_api)
    auto_register_api(app)


def init_jwt(app: OpenAPI):
    """init jwt"""
    from app.utils.jwt_tools import jwt_manager
    jwt_manager.init_app(app)


def init_db(app: OpenAPI):
    """init db"""
    from app.model import db
    db.init_app(app)


def init_rq2(app: OpenAPI):
    """init rq2"""
    from app.rq import rq2
    rq2.init_app(app)


def create_app():
    from . import config
    app = OpenAPI(
        __name__,
        info=Info(title=config.APP_NAME, version=config.APP_VERSION),
        security_schemes={
            "basic": {"type": "http", "scheme": "basic"},
            "jwt": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

        },
        doc_expansion="none",
    )

    app.json.ensure_ascii = False

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config.from_object(config)

    init_exception(app)

    CORS(app)

    init_jwt(app)

    init_db(app)

    init_rq2(app)

    register_apis(app)
    return app
