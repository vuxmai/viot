from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute


def setup_openapi(app: FastAPI) -> None:
    """Setup OpenAPI schema

    https://github.com/fastapi/fastapi/issues/3424#issuecomment-1287137297

    :param app:
    :return:
    """

    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        )
        for _, method_item in openapi_schema.get("paths").items():  # type: ignore
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove 422 response, also can remove other status codes
                if "422" in responses:
                    del responses["422"]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore
    simplify_operation_ids(app)


def simplify_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation ids to match the route name

    :param app:
    :return:
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
