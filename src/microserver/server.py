from __future__ import annotations

from .globals import _cv_microserver
from .models.blueprint import Blueprint
from .request_handler import MicroServerRequestHandler

from http.server import HTTPServer
import typing as t

if t.TYPE_CHECKING:
    from .models.response import Response


class MicroServer(Blueprint):
    """
    A lightweight Python webserver with minimal overhead and no external dependencies.
    """

    def __init__(self, *, route_prefix="/", views_dir = "views", static_dir = "static"):
        super().__init__(route_prefix=route_prefix, views_dir=views_dir, static_dir=static_dir)
        
        self.blueprints: list[Blueprint] = []
        self.error_handlers: dict[int, t.Callable[[], Response]] = {}

    def start(self, address: str, port: int):
        """
        Starts running the web server on the given address and port.
        """

        _cv_microserver.set(self)
        with HTTPServer((address, port), MicroServerRequestHandler) as server:
            server.serve_forever()

    def register_blueprint(self, blueprint: Blueprint):
        """
        Registers a `Blueprint` to be handled by the server.
        """

        self.blueprints.append(blueprint)

    def try_route(self, route: str, method: str) -> Response | None:
        """
        Calls try_route on every registered blueprint.
        See `Blueprint.try_route` for more details.
        """

        if response := super().try_route(route, method):
            return response
        
        for blueprint in self.blueprints:
            if response := blueprint.try_route(route, method):
                return response
            
    def errorhandler(self, code: int):
        """
        Configures the decorated function as the handler for all errors of the given code.
        The code must be `400 <= code < 600` as all HTTP errors fall within this range.
        """

        if code < 400 or code >= 600:
            raise ValueError(f"code must be 400 <= code < 600, got {code}")

        def wrapper(func):
            # Register the error handler and callback
            self.error_handlers[code] = func
            return func
        return wrapper
            
    def get_errorhandler(self, code: int) -> t.Callable[[], Response] | None:
        """
        Returns the errorhandler for the given code if one is registered.
        """

        return self.error_handlers.get(code, None)
