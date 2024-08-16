import dataclasses
from collections.abc import Callable
from functools import partial
from typing import Any, TypeVar

from classy_fastapi.routable import RoutableMeta
from classy_fastapi.route_args import EndpointDefinition, EndpointType
from fastapi.routing import APIRouter

AnyCallable = TypeVar("AnyCallable", bound=Callable[..., Any])


class Controller(metaclass=RoutableMeta):
    """Base class for all classes the want class-based routing.

    This Uses RoutableMeta as a metaclass and various decorators like @get or @post from the
    decorators module. The decorators just mark a method as an endpoint. The RoutableMeta then
    converts those to a list of desired endpoints in the _endpoints class method during class
    creation. The constructor constructs an APIRouter and adds all the routes in the _endpoints
    to it so they can be added to an app via FastAPI.include_router or similar.
    """

    _endpoints: list[EndpointDefinition] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.router = APIRouter(*args, **kwargs)
        for endpoint in self._endpoints:
            if endpoint.type() == EndpointType.WEBSOCKET:
                self.router.add_api_websocket_route(
                    path=endpoint.args.path,
                    endpoint=partial(endpoint.endpoint, self),
                    name=endpoint.args.name,
                )
            else:
                self.router.add_api_route(
                    endpoint=partial(endpoint.endpoint, self), **dataclasses.asdict(endpoint.args)
                )
