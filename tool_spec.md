# Tool Spec — mewcp-exa

## Auth type: static
## Timeout strategy: CONNECT_TIMEOUT=5, READ_TIMEOUT=30 (standard REST API)

## Group: core  →  core_tools.py
### search
- Endpoint: POST /search
- Description: Perform an Exa web search and return results. Takes a query and optional filters, returns matching web results with titles, URLs, and text snippets.
- Params: query (str, required): search query text; num_results (int, optional, default=10): number of results to return (1–100); include_domains (list[str], optional): only return results from these domains; exclude_domains (list[str], optional): exclude results from these domains; start_published_date (str, optional): ISO 8601 date — only return results published after this date; end_published_date (str, optional): ISO 8601 date — only return results published before this date; type (str, optional, default="auto"): search type — "keyword", "neural", or "auto"
- Response fields: results: list[SearchResult] — each with title: str, url: str, publishedDate: str, text: str, score: float, id: str; autoprompt: str | None; resolvedSearchType: str
- Tier: GET

### get_contents
- Endpoint: POST /contents
- Description: Extract clean, LLM-ready content (text, highlights, summaries) from URLs. Returns structured content per URL.
- Params: urls (list[str], required): list of URLs to retrieve content from; text_format (str, optional, default="text"): output format — "text", "html", or "markdown"; livecrawl (str, optional, default="fallback"): crawling mode — "always", "never", or "fallback"; highlight (dict, optional): highlight settings with sentences_per_highlight and highlights_per_url
- Response fields: results: list[ContentResult] — each with url: str, title: str, text: str, textLength: int, highlights: list[str] | None, summary: str | None, author: str | None; num_results: int
- Tier: GET

### get_answer
- Endpoint: POST /answer
- Description: Get an LLM answer to a question informed by Exa search results. Returns a generated answer with citations.
- Params: query (str, required): question to answer; text_format (str, optional, default="markdown"): answer format — "text" or "markdown"; include_domains (list[str], optional): only use sources from these domains; exclude_domains (list[str], optional): exclude sources from these domains; model (str, optional, default="exa-pro"): model to use for answer generation
- Response fields: answer: str; citations: list[Citation] — each with id: str, url: str, title: str, text: str, publishedDate: str | None; autoprompt: str | None
- Tier: GET

## Group: agent  →  agent_tools.py
### create_run
- Endpoint: POST /agent/runs
- Description: Creates a new Exa agent run. Starts an agent process that works toward a specified goal and returns the run details.
- Params: goal (str, required): the goal or task for the agent to complete; instructions (str, optional): additional instructions for the agent; model (str, optional, default="exa-pro"): model to use; max_steps (int, optional, default=20): maximum number of steps the agent can take; temperature (float, optional, default=0.7): temperature for the model
- Response fields: id: str; status: str; goal: str; created_at: str; model: str; max_steps: int
- Tier: CREATE

### get_run
- Endpoint: GET /agent/runs/{id}
- Description: Retrieves the details of a specific agent run. Returns run status, goal, and result if completed.
- Params: id (str, required): the ID of the run to retrieve
- Response fields: id: str; status: str; goal: str; created_at: str; updated_at: str | None; completed_at: str | None; result: str | None; model: str; max_steps: int
- Tier: GET

### list_runs
- Endpoint: GET /agent/runs
- Description: Retrieves a list of agent runs. Returns runs with their current status and basic metadata.
- Params: limit (int, optional, default=20): maximum number of runs to return (1–100); offset (int, optional, default=0): pagination offset
- Response fields: runs: list[RunSummary] — each with id: str, status: str, goal: str, created_at: str, updated_at: str | None; total: int | None
- Tier: GET

### cancel_run
- Endpoint: POST /agent/runs/{id}/cancel
- Description: Cancels an in-progress agent run. Stops the agent's execution and updates the run status.
- Params: id (str, required): the ID of the run to cancel
- Response fields: id: str; status: str; previous_status: str
- Tier: UPDATE

### delete_run
- Endpoint: DELETE /agent/runs/{id}
- Description: DESTRUCTIVE — Permanently deletes an existing agent run. This action is irreversible. The run record and all associated data will be permanently removed.
- Params: id (str, required): the ID of the run to delete
- Response fields: id: str; deleted: bool
- Tier: DELETE

### list_run_events
- Endpoint: GET /agent/runs/{id}/events
- Description: Retrieves a list of events for a specific agent run. Returns chronological events including steps, tool calls, and results.
- Params: id (str, required): the ID of the run to get events for; limit (int, optional, default=50): maximum events to return (1–200); offset (int, optional, default=0): pagination offset
- Response fields: events: list[RunEvent] — each with id: str, type: str, created_at: str, data: dict | None; total: int | None
- Tier: GET