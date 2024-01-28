from __future__ import annotations

from .response import Response
from .route import Route

import mimetypes
import os.path as path

class Blueprint:
    """
    A MicroServer routing component that tracks configured routes.

    Each `Blueprint` can have custom views and static directories.
    Directories are relative to the CWD unless they are absolute.

    A custom route prefix can be specified to separate URLs.
    ```py
    admin = Blueprint(route_prefix="/admin")

    # Registers this method to handle /admin/dashboard
    @admin.route("/dashboard")
    def dashboard():
        pass
    ```
    """

    def __init__(self, *, route_prefix="/", views_dir="views", static_dir="static"):
        self.route_prefix = route_prefix
        self.views_dir = views_dir
        self.static_dir = static_dir

        self.routes: list[Route] = []

    def route(self, route: str, *, methods: list[str] = ["GET"]):
        """
        Configures the decorated function as the handler for the given route.

        Valid methods are: `GET` `HEAD` `POST` `PUT` `DELETE` `CONNECT` `OPTIONS` `TRACE` `PATCH`
        """

        def wrapper(func):
            _route = route.strip("/")
            _prefix = self.route_prefix.strip("/")
            resolved_route = f"/{_prefix}/{route}" if _prefix != "" else f"/{_route}"

            # Register the route and callback
            self.routes.append(Route(resolved_route, func, methods))
            return func
        return wrapper

    def try_route(self, route: str, method: str) -> Response | None:
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
            else: # only executes if break is not hit
                if method not in r.methods:
                    return Response.for_status(405) # Method not allowed
                
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
