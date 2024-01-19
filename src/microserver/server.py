from .http_server import MicroServerHTTPServer
from .response import Response
from .request_handler import MicroServerRequestHandler
from .route import Route

import mimetypes
import os.path as path
from typing import Callable

class MicroServer:
    """
    A lightweight Python webserver with minimal overhead and no external dependencies.
    """

    def __init__(self, *, views_dir = "views", static_dir = "static"):
        self.views_dir = views_dir
        self.static_dir = static_dir

        self.routes: list[Route] = []
        self.error_handlers: dict[int, Callable[[], str]] = {}

    def start(self, address: str, port: int):
        """
        Starts running the web server on the given address and port.
        """

        with MicroServerHTTPServer((address, port), MicroServerRequestHandler, self) as server:
            server.serve_forever()

    def route(self, route: str):
        """
        Configures the decorated function as the handler for the given route.
        """

        def wrapper(func):
            # Register the route and callback
            self.routes.append(Route(route, func))
            return func
        return wrapper

    def errorhandler(self, code: int):
        """
        Configures the decorated function as the handler for all errors of the given code.
        """

        def wrapper(func):
            # Register the error handler and callback
            self.error_handlers[code] = func
            return func
        return wrapper

    def get_route(self, route: str) -> Response | None:
        """
        Runs the callback for a given route to get the view.
        Resolves parameterized routes appropriately.

        Returns a `Response` if the route was valid, else `None`.
        """

        parts = route.split("/")
        for r in self.routes:
            r_parts = r.route.split("/")
            if len(r_parts) != len(parts):
                continue
            
            params = []
            for part, r_part in zip(parts, r_parts):
                if r_part.startswith("{") and r_part.endswith("}"):
                    params.append(part)
                elif part != r_part:
                    break
            else:
                # only executes if break is not hit
                return r.handler(*params)
    
    def get_static(self, filename: str) -> Response | None:
        """
        Reads the file data for a given filename.

        Returns a `Response` if the file exists, else `None`.
        """

        # Drop leading /
        if filename.startswith("/"):
            filename = filename[1:]

        # Check the file is in the static directory
        if not filename.startswith(self.static_dir):
            return None
        
        try:
            with open(filename, "r") as f:
                data = "".join(f.readlines())
            mime, _ = mimetypes.guess_type(filename)
            return Response(data, mime)
        except OSError:
            return None
    
    def load_view(self, filename: str) -> str:
        """
        Reads the given file relative to `self.views_dir` and returns its contents.
        """

        file_path = path.join(self.views_dir, filename)
        with open(file_path, "r") as f:
            return "".join(f.readlines())
