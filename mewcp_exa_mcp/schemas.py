"""Pydantic models for MewCP Exa MCP Server."""

from pydantic import BaseModel, ConfigDict
from typing import Any


# ── Base classes ──────────────────────────────────────────────────────────

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# ── Core group: SearchResult ──────────────────────────────────────────────

class SearchResultItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = None
    url: str | None = None
    publishedDate: str | None = None
    text: str | None = None
    score: float | None = None
    id: str | None = None


class SearchData(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[SearchResultItem] = []
    autoprompt: str | None = None
    resolvedSearchType: str | None = None


class SearchResult(ToolResult):
    data: SearchData | None = None


# ── Core group: ContentResult ─────────────────────────────────────────────

class ContentResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    url: str | None = None
    title: str | None = None
    text: str | None = None
    textLength: int | None = None
    highlights: list[str] | None = None
    summary: str | None = None
    author: str | None = None


class ContentsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    results: list[ContentResult] = []
    num_results: int | None = None


class ContentsResult(ToolResult):
    data: ContentsData | None = None


# ── Core group: AnswerResult ──────────────────────────────────────────────

class Citation(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    url: str | None = None
    title: str | None = None
    text: str | None = None
    publishedDate: str | None = None


class AnswerData(BaseModel):
    model_config = ConfigDict(extra="allow")

    answer: str | None = None
    citations: list[Citation] = []
    autoprompt: str | None = None


class AnswerResult(ToolResult):
    data: AnswerData | None = None


# ── Agent group: Run ──────────────────────────────────────────────────────

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


# ── Agent group: Run list ─────────────────────────────────────────────────

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


# ── Agent group: Run cancel ───────────────────────────────────────────────

class RunCancelData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    status: str | None = None
    previous_status: str | None = None


class RunCancelResult(ToolResult):
    data: RunCancelData | None = None


# ── Agent group: Run delete ───────────────────────────────────────────────

class RunDeleteData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    deleted: bool | None = None


class RunDeleteResult(ToolResult):
    data: RunDeleteData | None = None


# ── Agent group: Run events ───────────────────────────────────────────────

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