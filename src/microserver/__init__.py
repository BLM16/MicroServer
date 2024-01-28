"""
A lightweight Python webserver with minimal overhead and no external dependencies.
"""

from __future__ import annotations

from .globals import request
from .server import MicroServer
from .models.blueprint import Blueprint
from .models.response import Response
