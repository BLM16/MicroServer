from .response import Response

from typing import Callable, Any

class Route:
    """
    Contains the routing information for a registered route.
    """

    def __init__(self, route: str, handler: Callable[[Any], Response]):
        self.route = route
        self.handler = handler
