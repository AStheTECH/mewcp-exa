from typing import Any

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class RunData(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    status: str | None = None
    goal: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    completed_at: str | None = None
    result: str | None = None
    model: str | None = None
    max_steps: int | None = None

class RunResult(ToolResult):
    data: RunData | None = None

class RunSummary(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    status: str | None = None
    goal: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

class RunListData(BaseModel):
    model_config = ConfigDict(extra="allow")
    runs: list[RunSummary] = []
    total: int | None = None

class RunListResult(ToolResult):
    data: RunListData | None = None

class RunCancelData(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    status: str | None = None
    previous_status: str | None = None

class RunCancelResult(ToolResult):
    data: RunCancelData | None = None

class RunDeleteData(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    deleted: bool | None = None

class RunDeleteResult(ToolResult):
    data: RunDeleteData | None = None

class RunEvent(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    type: str | None = None
    created_at: str | None = None
    data: dict[str, Any] | None = None

class RunEventListData(BaseModel):
    model_config = ConfigDict(extra="allow")
    events: list[RunEvent] = []
    total: int | None = None

class RunEventListResult(ToolResult):
    data: RunEventListData | None = None
