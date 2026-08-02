"""Core group: search, get_contents, get_answer"""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


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
