"""Local-first skill router for coding agents.

Pick at most one skill (or none). No API by default.
Optional semantic judge (e.g. TypeSafe Jev) only when local is unsure.
"""

from .router import route, parse_catalog

__all__ = ["route", "parse_catalog"]
__version__ = "0.1.0"
