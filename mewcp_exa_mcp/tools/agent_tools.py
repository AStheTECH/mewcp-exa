"""Agent group: create_run, get_run, list_runs, cancel_run, delete_run, list_run_events"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.agent import (
    RunResult, RunData, RunListResult, RunListData, RunSummary,
    RunCancelResult, RunCancelData, RunDeleteResult, RunDeleteData,
    RunEventListResult, RunEventListData, RunEvent,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("exa-mcp.tools.agent")


def register_agent_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_run",
        description=(
            "Creates a new Exa agent run. "
            "Starts an agent process that works toward a specified goal and returns the run details. "
            "Use the returned run ID to check status, list events, or cancel the run."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True),
    )
    def create_run(
        goal: str = Field(description="The goal or task for the agent to complete."),
        instructions: str | None = Field(default=None, description="Additional instructions for the agent."),
        model: str | None = Field(default="exa-pro", description="Model to use for the agent."),
        max_steps: int | None = Field(default=20, description="Maximum number of steps the agent can take (1–100)."),
        temperature: float | None = Field(default=0.7, description="Temperature for the model (0.0–1.0)."),
    ) -> RunResult:
        tlog = ToolLogger(logger, "create_run")

        if not goal:
            return _err(RunResult, tlog, "VALIDATION_ERROR", "goal must not be empty", 400)
        if max_steps and (max_steps < 1 or max_steps > 100):
            return _err(RunResult, tlog, "VALIDATION_ERROR", "max_steps must be 1–100", 400)
        if temperature and (temperature < 0.0 or temperature > 1.0):
            return _err(RunResult, tlog, "VALIDATION_ERROR", "temperature must be 0.0–1.0", 400)

        body = {"goal": goal}
        if instructions:
            body["instructions"] = instructions
        if model:
            body["model"] = model
        if max_steps is not None:
            body["maxSteps"] = max_steps
        if temperature is not None:
            body["temperature"] = temperature

        try:
            data, status, retry_after = service.api_request(
                "POST", "/agent/runs", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunResult(success=True, statusCode=status, data=RunData(**data))
            return _upstream_err(RunResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunResult, tlog, exc)

    @mcp.tool(
        name="get_run",
        description=(
            "Retrieves the details of a specific agent run. "
            "Returns run status, goal, model, and result if completed. "
            "Use to check whether a run has finished or to get its output."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_run(
        id: str = Field(description="The ID of the run to retrieve."),
    ) -> RunResult:
        tlog = ToolLogger(logger, "get_run")

        if not id:
            return _err(RunResult, tlog, "VALIDATION_ERROR", "id must not be empty", 400)

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/agent/runs/{id}",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunResult(success=True, statusCode=status, data=RunData(**data))
            return _upstream_err(RunResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunResult, tlog, exc)

    @mcp.tool(
        name="list_runs",
        description=(
            "Retrieves a list of agent runs. "
            "Returns runs with their current status, goal, and creation timestamps. "
            "Use to browse all runs and find specific ones by their IDs."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_runs(
        limit: int = Field(default=20, description="Maximum number of runs to return (1–100)."),
        offset: int = Field(default=0, description="Pagination offset."),
    ) -> RunListResult:
        tlog = ToolLogger(logger, "list_runs")

        if limit < 1 or limit > 100:
            return _err(RunListResult, tlog, "VALIDATION_ERROR", "limit must be 1–100", 400)
        if offset < 0:
            return _err(RunListResult, tlog, "VALIDATION_ERROR", "offset must be non-negative", 400)

        params = {"limit": limit, "offset": offset}

        try:
            data, status, retry_after = service.api_request(
                "GET", "/agent/runs", params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunListResult(success=True, statusCode=status, data=RunListData(**data))
            return _upstream_err(RunListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunListResult, tlog, exc)

    @mcp.tool(
        name="cancel_run",
        description=(
            "Cancels an in-progress agent run. "
            "Stops the agent's execution and updates the run status. "
            "The response includes both the previous and current status."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def cancel_run(
        id: str = Field(description="The ID of the run to cancel."),
    ) -> RunCancelResult:
        tlog = ToolLogger(logger, "cancel_run")

        if not id:
            return _err(RunCancelResult, tlog, "VALIDATION_ERROR", "id must not be empty", 400)

        try:
            data, status, retry_after = service.api_request(
                "POST", f"/agent/runs/{id}/cancel",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunCancelResult(success=True, statusCode=status, data=RunCancelData(**data))
            return _upstream_err(RunCancelResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunCancelResult, tlog, exc)

    @mcp.tool(
        name="delete_run",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes an existing agent run. "
            "This action is irreversible — the run record and all associated data will be permanently removed. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_run(
        id: str = Field(description="The ID of the run to delete."),
    ) -> RunDeleteResult:
        tlog = ToolLogger(logger, "delete_run")

        if not id:
            return _err(RunDeleteResult, tlog, "VALIDATION_ERROR", "id must not be empty", 400)

        try:
            data, status, retry_after = service.api_request(
                "DELETE", f"/agent/runs/{id}",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunDeleteResult(success=True, statusCode=status, data=RunDeleteData(**data))
            return _upstream_err(RunDeleteResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunDeleteResult, tlog, exc)

    @mcp.tool(
        name="list_run_events",
        description=(
            "Retrieves a list of events for a specific agent run. "
            "Returns chronological events including steps, tool calls, and results. "
            "Use to monitor run progress or inspect what the agent did."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_run_events(
        id: str = Field(description="The ID of the run to get events for."),
        limit: int = Field(default=50, description="Maximum events to return (1–200)."),
        offset: int = Field(default=0, description="Pagination offset."),
    ) -> RunEventListResult:
        tlog = ToolLogger(logger, "list_run_events")

        if not id:
            return _err(RunEventListResult, tlog, "VALIDATION_ERROR", "id must not be empty", 400)
        if limit < 1 or limit > 200:
            return _err(RunEventListResult, tlog, "VALIDATION_ERROR", "limit must be 1–200", 400)
        if offset < 0:
            return _err(RunEventListResult, tlog, "VALIDATION_ERROR", "offset must be non-negative", 400)

        params = {"limit": limit, "offset": offset}

        try:
            data, status, retry_after = service.api_request(
                "GET", f"/agent/runs/{id}/events", params=params,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return RunEventListResult(success=True, statusCode=status, data=RunEventListData(**data))
            return _upstream_err(RunEventListResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(RunEventListResult, tlog, exc)