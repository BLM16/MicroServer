from __future__ import annotations

import cgi
from http import cookies
import typing as t

if t.TYPE_CHECKING:
    from ..request_handler import MicroServerRequestHandler

class Request:
    """
    Contains the information to be passed to the user about the
    HTTP request that was made to the server.
    """

    method: str
    headers: MicroServerRequestHandler.MessageClass
    path: str
    cookies: cookies.SimpleCookie
    form: cgi.FieldStorage

    @classmethod
    def from_http_request(cls, req: MicroServerRequestHandler):
        r = cls()
        r.method = req.command
        r.headers = req.headers
        r.path = req.path
        r.cookies = cookies.SimpleCookie(req.headers.get("Cookie"))

        if req.command == "POST":
            r.form = cgi.FieldStorage(
                fp=req.rfile,
                headers=req.headers,
                environ={
                    "REQUEST_METHOD": req.command,
                    "CONTENT_TYPE": req.headers.get("Content-Type")
                }
            )

        return r
