from http.server import HTTPServer, BaseHTTPRequestHandler

class MicroServerHTTPServer(HTTPServer):
    """
    Wraper for the `HTTPServer` that injects the active `MicroServer` instance
    for use by the `MicroServerRequestHandler`.
    """

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass: BaseHTTPRequestHandler, microserver):
        super().__init__(server_address, RequestHandlerClass)
        self.microserver = microserver
