"""Core group: search, get_contents, get_answer"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.core import SearchResult, SearchData, SearchResultItem, ContentsResult, ContentsData, ContentResult, AnswerResult, AnswerData, Citation
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("exa-mcp.tools.core")


def register_core_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="search",
        description=(
            "Perform an Exa web search and return results. "
            "Takes a query and optional filters for domain inclusion/exclusion, date range, and search type. "
            "Returns matching web results with titles, URLs, published dates, and text snippets. "
            "Use `autoprompt` from the response to refine or repeat the search."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def search(
        query: str = Field(description="The search query text."),
        num_results: int = Field(default=10, description="Number of results to return (1–100)."),
        include_domains: list[str] | None = Field(default=None, description="Only return results from these domains."),
        exclude_domains: list[str] | None = Field(default=None, description="Exclude results from these domains."),
        start_published_date: str | None = Field(default=None, description="ISO 8601 date — only return results published after this date."),
        end_published_date: str | None = Field(default=None, description="ISO 8601 date — only return results published before this date."),
        type: str | None = Field(default="auto", description="Search type: 'keyword', 'neural', or 'auto'."),
    ) -> SearchResult:
        tlog = ToolLogger(logger, "search")

        if num_results < 1 or num_results > 100:
            return _err(SearchResult, tlog, "VALIDATION_ERROR", "num_results must be 1–100", 400)
        if type and type not in ("keyword", "neural", "auto"):
            return _err(SearchResult, tlog, "VALIDATION_ERROR", "type must be 'keyword', 'neural', or 'auto'", 400)

        body = {"query": query}
        if num_results != 10:
            body["numResults"] = num_results
        if include_domains:
            body["includeDomains"] = include_domains
        if exclude_domains:
            body["excludeDomains"] = exclude_domains
        if start_published_date:
            body["startPublishedDate"] = start_published_date
        if end_published_date:
            body["endPublishedDate"] = end_published_date
        if type:
            body["type"] = type

        try:
            data, status, retry_after = service.api_request(
                "POST", "/search", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return SearchResult(success=True, statusCode=status, data=SearchData(**data))
            return _upstream_err(SearchResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(SearchResult, tlog, exc)

    @mcp.tool(
        name="get_contents",
        description=(
            "Extract clean, LLM-ready content from URLs. "
            "Returns structured content per URL including text, highlights, and summaries. "
            "Supports text, HTML, or markdown output formats."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_contents(
        urls: list[str] = Field(description="List of URLs to retrieve content from."),
        text_format: str | None = Field(default="text", description="Output format: 'text', 'html', or 'markdown'."),
        livecrawl: str | None = Field(default="fallback", description="Crawling mode: 'always', 'never', or 'fallback'."),
        highlight: dict | None = Field(default=None, description="Highlight settings with sentences_per_highlight and highlights_per_url."),
    ) -> ContentsResult:
        tlog = ToolLogger(logger, "get_contents")

        if not urls:
            return _err(ContentsResult, tlog, "VALIDATION_ERROR", "urls must not be empty", 400)
        if text_format and text_format not in ("text", "html", "markdown"):
            return _err(ContentsResult, tlog, "VALIDATION_ERROR", "text_format must be 'text', 'html', or 'markdown'", 400)
        if livecrawl and livecrawl not in ("always", "never", "fallback"):
            return _err(ContentsResult, tlog, "VALIDATION_ERROR", "livecrawl must be 'always', 'never', or 'fallback'", 400)

        body = {"urls": urls}
        if text_format:
            body["textFormat"] = text_format
        if livecrawl:
            body["livecrawl"] = livecrawl
        if highlight:
            body["highlight"] = highlight

        try:
            data, status, retry_after = service.api_request(
                "POST", "/contents", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return ContentsResult(success=True, statusCode=status, data=ContentsData(**data))
            return _upstream_err(ContentsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ContentsResult, tlog, exc)

    @mcp.tool(
        name="get_answer",
        description=(
            "Get an LLM answer to a question informed by Exa search results. "
            "Returns a generated answer text with citations from source URLs. "
            "Use for Q&A, research, and fact-finding tasks."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_answer(
        query: str = Field(description="The question to answer."),
        text_format: str | None = Field(default="markdown", description="Answer format: 'text' or 'markdown'."),
        include_domains: list[str] | None = Field(default=None, description="Only use sources from these domains."),
        exclude_domains: list[str] | None = Field(default=None, description="Exclude sources from these domains."),
        model: str | None = Field(default="exa-pro", description="Model to use for answer generation."),
    ) -> AnswerResult:
        tlog = ToolLogger(logger, "get_answer")

        if not query:
            return _err(AnswerResult, tlog, "VALIDATION_ERROR", "query must not be empty", 400)
        if text_format and text_format not in ("text", "markdown"):
            return _err(AnswerResult, tlog, "VALIDATION_ERROR", "text_format must be 'text' or 'markdown'", 400)

        body = {"query": query}
        if text_format:
            body["textFormat"] = text_format
        if include_domains:
            body["includeDomains"] = include_domains
        if exclude_domains:
            body["excludeDomains"] = exclude_domains
        if model:
            body["model"] = model

        try:
            data, status, retry_after = service.api_request(
                "POST", "/answer", body=body,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return AnswerResult(success=True, statusCode=status, data=AnswerData(**data))
            return _upstream_err(AnswerResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(AnswerResult, tlog, exc)