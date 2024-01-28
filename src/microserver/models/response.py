from __future__ import annotations

from http import cookies

class Response:
    """
    All server routes and error handlers must return a `Response`.
    Tracks the return data and corresponding server information.
    """

    def __init__(self, data: str, mime: str, *, status=200):
        self.data = data
        self.mime = mime
        self.status = status

        self.new_cookies = cookies.SimpleCookie()
        self.redirect_path: str | None = None

    def add_cookie(self, key: str, value: str):
        """
        Adds a Set-Cookie header for the given key:value to the response.
        """

        self.new_cookies[key] = value

    @classmethod
    def redirect(cls, path: str, *, status=302):
        """
        Creates a `Response` that redirects a client to the given path.

        A 302 Found is the default status code.
        Consider using 303 if you are redirecting from a POST.
        """

        c = cls("", "", status=status)
        c.redirect_path = path
        return c

    @classmethod
    def for_status(cls, status: int):
        """
        Creates a `Response` with only a status code.

        Suggested use is for simple 400 and 500 series errors
        where no further response parameters are required.
        """

        return cls("", "", status=status)
