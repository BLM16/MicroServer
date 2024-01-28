from __future__ import annotations

from .globals import _cv_request, microserver
from .models.request import Request

from http.server import BaseHTTPRequestHandler
import importlib.metadata as metadata

class MicroServerRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the MicroServer.
    
    Provides custom implementations for the following requests:
    `GET` `HEAD` `POST` `PUT` `DELETE` `CONNECT` `OPTIONS` `TRACE` `PATCH`
    """
    
    server_version = f"MicroServer/{metadata.version("BLM16-MicroServer")}"

    def handle_routing_for(self, method):
        """
        Tries to call the registered handler for the requested URL.

        - Calls the registered handler for the route if it exists.
            - Calls the corresponding errorhandler if response.status in [400, 600).
            - Returns the corresponding response.data for success codes.
        - Calls the registered 404 handler if it exists.
        - Returns a basic 404 error as a fallthrough.
        """

        _cv_request.set(Request.from_http_request(self))

        if response := microserver.try_route(self.path, method):
            # Handle redirect responses
            if response.redirect_path is not None:
                self.send_response(response.status)
                self.send_header("Location", response.redirect_path)
                for morsel in response.new_cookies.values():
                    self.send_header("Set-Cookie", morsel.output(header=""))
                self.end_headers()
                return

            if response.status >= 400:
                # Call error handler if one is defined
                if errorhandler := microserver.get_errorhandler(response.status):
                    response = errorhandler()

                    self.send_response(response.status)
                    self.send_header("Content-Type", response.mime)
                    for cookie in response.new_cookies.values():
                        self.send_header("Set-Cookie", cookie.output(header=""))
                    self.end_headers()

                    self.wfile.write(bytes(response.data, "utf-8"))
                    return

            self.send_response(response.status)
            self.send_header("Content-Type", response.mime)
            for morsel in response.new_cookies.values():
                self.send_header("Set-Cookie", morsel.output(header=""))
            self.end_headers()

            self.wfile.write(bytes(response.data, "utf-8"))
            return
        
        # Call 404 handler if one is defined
        if errorhandler := microserver.get_errorhandler(404):
            response = errorhandler()

            self.send_response(404)
            self.send_header("Content-Type", response.mime)
            for cookie in response.new_cookies.values():
                self.send_header("Set-Cookie", cookie.output(header=""))
            self.end_headers()

            self.wfile.write(bytes(response.data, "utf-8"))
            return

        # Fallthrough
        self.send_error(404, "Not found")

    def do_GET(self):        
        # Return static file if appropriate
        if response := microserver.get_static(self.path):
            self.send_response(response.status)
            self.send_header("Content-Type", response.mime)
            for cookie in response.new_cookies.values():
                self.send_header("Set-Cookie", cookie.output(header=""))
            self.end_headers()
            self.wfile.write(bytes(response.data, "utf-8"))
            return

        self.handle_routing_for("GET")
    
    def do_HEAD(self):
        self.handle_routing_for("HEAD")

    def do_POST(self):
        self.handle_routing_for("POST")

    def do_PUT(self):
        self.handle_routing_for("PUT")

    def do_DELETE(self):
        self.handle_routing_for("DELETE")

    def do_CONNECT(self):
        self.handle_routing_for("CONNECT")

    def do_OPTIONS(self):
        self.handle_routing_for("OPTIONS")

    def do_TRACE(self):
        self.handle_routing_for("TRACE")

    def do_PATCH(self):
        self.handle_routing_for("PATCH")
