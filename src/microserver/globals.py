from __future__ import annotations

from .util.proxy_var import ProxyVar

from contextvars import ContextVar
import typing as t

if t.TYPE_CHECKING:
    from .models.request import Request
    from .server import MicroServer

# Contains information such as headers and the http method
# for the request the server is actively handling.
_cv_request: ContextVar[Request] = ContextVar('request', default=None)
request: Request = ProxyVar(_cv_request.get)

# Contains the active MicroServer instance
_cv_microserver: ContextVar[MicroServer] = ContextVar('microserver', default=None)
microserver: MicroServer = ProxyVar(_cv_microserver.get)
