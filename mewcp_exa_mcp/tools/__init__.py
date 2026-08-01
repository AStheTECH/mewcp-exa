"""MewCP Exa tool registration."""

from fastmcp import FastMCP

from .core_tools import register_core_tools
from .agent_tools import register_agent_tools


def register_tools(mcp: FastMCP) -> None:
    register_core_tools(mcp)
    register_agent_tools(mcp)