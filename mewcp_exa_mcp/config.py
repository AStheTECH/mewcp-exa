"""Configuration for MewCP Exa MCP Server."""

import logging
import os

SERVER_VERSION = "v2.0.0"
BREAKING_CHANGES: list[dict] = [
    {
        "version": "v2.0.0",
        "change": "Renamed tool 'search' to 'search_web' for verb_noun naming consistency.",
    },
]

EXA_API_BASE = "https://api.exa.ai"

# Standard REST API — Exa responds within a few seconds for most queries
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)