from __future__ import annotations

import typing as t

class ProxyVar[_T]:
    """
    Acts as whatever object is returned from the callback.

    Callback is computed for every access, similar to a class property.
    """

    def __init__(self, cb: t.Callable[[], _T]):
        self.cb = cb

    def __getattr__(self, name):
        return getattr(self.cb(), name)
