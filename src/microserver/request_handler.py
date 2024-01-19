from http.server import BaseHTTPRequestHandler
import importlib.metadata as metadata

class MicroServerRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the MicroServer.
    
    Provides custom implementations for the following requests: `GET`
    """
    
    server_version = f"MicroServer/{metadata.version("BLM16-MicroServer")}"

    def do_GET(self):
        """
        Handles GET requests made to the `MicroServer`.

        - Renders a static file if the route matches `MicroServer.static_dir`.
        - Renders the corresponding view if the route is configured.

        If the path is not a static file or a registered view:
        - Renders the registered 404 error handler if it exists.
        - Renders a default 404 page as a last resort.
        """

        # Test static file
        if response := self.server.microserver.get_static(self.path):
            self.send_response(200)
            self.send_header("Content-Type", response.mime)
            self.end_headers()
            self.wfile.write(bytes(response.data, "utf-8"))
            return
        
        # Test routed view
        if response := self.server.microserver.get_route(self.path):
            self.send_response(200)
            self.send_header("Content-Type", response.mime)
            self.end_headers()
            self.wfile.write(bytes(response.data, "utf-8"))
            return    
    
        # No 404 handler was defined
        if 404 not in self.server.microserver.error_handlers:
            self.send_error(404, "Not found")
            return
        
        # Send the 404 handler
        response = self.server.microserver.error_handlers[404]()

        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(response.data, "utf-8"))