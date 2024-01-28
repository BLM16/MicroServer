from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .response import Response

class Route:
    """
    Contains the routing information for a registered route.
    """

    def __init__(self, route: str, handler: t.Callable[..., Response], methods: list[str]):
        self.route = route
        self.handler = handler
        self.methods = methods
