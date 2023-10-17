#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from py_bife.myconfig import MyConfig

my_config = MyConfig()
my_config.fix_workers()


app = FastAPI(docs_url="/swagger")


def create_app() -> FastAPI:
    from py_bife.model.user import User
    from py_bife.model.message import Message
    from py_bife.database.database import migrate

    migrate()

    from py_bife.application.user_api import user_router
    from py_bife.application.message_api import message_router

    app.include_router(user_router)
    app.include_router(message_router)
    app.openapi_schema = custom_openapi_schema()

    return app


def custom_openapi_schema():
    tags_metadata = [
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "messages",
            "description": "Operations related with the messages",
        },
    ]
    return get_openapi(
        title="py-bife",
        routes=app.routes,
        version="0.0.1",
        summary="Simple API",
        description="A simple POC for a messages system based on FastApi",
        tags=tags_metadata,
        contact={
            "name": "Juan Knebel",
            "url": "https://github.com/juanknebel/py-bife",
            "email": "juanknebel@gmail.com",
        },
        servers=[
            {"description": "Local server", "url": "http://localhost:5000"},
            {"description": "Production", "url": "http://localhost:8080"},
        ],
    )
