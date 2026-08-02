**Search the web and extract content with Exa's AI-powered search engine.**

A Model Context Protocol (MCP) server that exposes Exa's API for web search, content extraction, and AI-powered agent runs.

## Overview

The MewCP Exa MCP Server provides AI-powered web search and content extraction:

- **Web Search** — Perform semantic and keyword searches across the web with domain filtering and date range constraints
- **Content Extraction** — Extract clean, LLM-ready content (text, highlights, summaries) from URLs
- **AI Answer Generation** — Get LLM-generated answers to questions informed by search results
- **Agent Runs** — Create and manage autonomous AI agents that work toward specified goals

Perfect for:

- Research and fact-checking tasks that need up-to-date web information
- Content aggregation pipelines that extract structured data from URLs
- Q&A systems that need grounded answers with source citations
- Automated research agents that browse, search, and synthesize information

## Tools


<details>
<summary><code>search_web</code> — Perform an Exa web search and return results</summary>

Perform an Exa web search and return results. Takes a query and optional filters for domain inclusion/exclusion, date range, and search type. Returns matching web results with titles, URLs, published dates, and text snippets. Use `autoprompt` from the response to refine or repeat the search.

**Inputs:**
```
- `query` (str, required) — The search query text.
- `num_results` (int, optional, default: 10) — Number of results to return (1–100).
- `include_domains` (list[str], optional) — Only return results from these domains.
- `exclude_domains` (list[str], optional) — Exclude results from these domains.
- `start_published_date` (str, optional) — ISO 8601 date — only return results published after this date.
- `end_published_date` (str, optional) — ISO 8601 date — only return results published before this date.
- `type` (str, optional, default: "auto") — Search type: 'keyword', 'neural', or 'auto'.
```

**Output `data` schema:**

```typescript
{
  results: {
    title: string | null;
    url: string | null;
    publishedDate: string | null;
    text: string | null;
    score: number | null;
    id: string | null;
  }[];
  autoprompt: string | null;
  resolvedSearchType: string | null;
}
```

</details>


<details>
<summary><code>get_contents</code> — Extract clean, LLM-ready content from URLs</summary>

Extract clean, LLM-ready content from URLs. Returns structured content per URL including text, highlights, and summaries. Supports text, HTML, or markdown output formats.

**Inputs:**
```
- `urls` (list[str], required) — List of URLs to retrieve content from.
- `text_format` (str, optional, default: "text") — Output format: 'text', 'html', or 'markdown'.
- `livecrawl` (str, optional, default: "fallback") — Crawling mode: 'always', 'never', or 'fallback'.
- `highlight` (dict, optional) — Highlight settings with sentences_per_highlight and highlights_per_url.
```

**Output `data` schema:**

```typescript
{
  results: {
    url: string | null;
    title: string | null;
    text: string | null;
    textLength: number | null;
    highlights: string[] | null;
    summary: string | null;
    author: string | null;
  }[];
  num_results: number | null;
}
```

</details>


<details>
<summary><code>get_answer</code> — Get an LLM answer to a question informed by Exa search results</summary>

Get an LLM answer to a question informed by Exa search results. Returns a generated answer text with citations from source URLs. Use for Q&A, research, and fact-finding tasks.

**Inputs:**
```
- `query` (str, required) — The question to answer.
- `text_format` (str, optional, default: "markdown") — Answer format: 'text' or 'markdown'.
- `include_domains` (list[str], optional) — Only use sources from these domains.
- `exclude_domains` (list[str], optional) — Exclude sources from these domains.
- `model` (str, optional, default: "exa-pro") — Model to use for answer generation.
```

**Output `data` schema:**

```typescript
{
  answer: string | null;
  citations: {
    id: string | null;
    url: string | null;
    title: string | null;
    text: string | null;
    publishedDate: string | null;
  }[];
  autoprompt: string | null;
}
```

</details>


<details>
<summary><code>create_run</code> — Creates a new Exa agent run</summary>

Creates a new Exa agent run. Starts an agent process that works toward a specified goal and returns the run details. Use the returned run ID to check status, list events, or cancel the run.

**Inputs:**
```
- `goal` (str, required) — The goal or task for the agent to complete.
- `instructions` (str, optional) — Additional instructions for the agent.
- `model` (str, optional, default: "exa-pro") — Model to use for the agent.
- `max_steps` (int, optional, default: 20) — Maximum number of steps the agent can take (1–100).
- `temperature` (float, optional, default: 0.7) — Temperature for the model (0.0–1.0).
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  status: string | null;
  goal: string | null;
  created_at: string | null;
  updated_at: string | null;
  completed_at: string | null;
  result: string | null;
  model: string | null;
  max_steps: number | null;
}
```

</details>


<details>
<summary><code>get_run</code> — Retrieves the details of a specific agent run</summary>

Retrieves the details of a specific agent run. Returns run status, goal, model, and result if completed. Use to check whether a run has finished or to get its output.

**Inputs:**
```
- `id` (str, required) — The ID of the run to retrieve.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  status: string | null;
  goal: string | null;
  created_at: string | null;
  updated_at: string | null;
  completed_at: string | null;
  result: string | null;
  model: string | null;
  max_steps: number | null;
}
```

</details>


<details>
<summary><code>list_runs</code> — Retrieves a list of agent runs</summary>

Retrieves a list of agent runs. Returns runs with their current status, goal, and creation timestamps. Use to browse all runs and find specific ones by their IDs.

**Inputs:**
```
- `limit` (int, optional, default: 20) — Maximum number of runs to return (1–100).
- `offset` (int, optional, default: 0) — Pagination offset.
```

**Output `data` schema:**

```typescript
{
  runs: {
    id: string | null;
    status: string | null;
    goal: string | null;
    created_at: string | null;
    updated_at: string | null;
  }[];
  total: number | null;
}
```

</details>


<details>
<summary><code>cancel_run</code> — Cancels an in-progress agent run</summary>

Cancels an in-progress agent run. Stops the agent's execution and updates the run status. The response includes both the previous and current status.

**Inputs:**
```
- `id` (str, required) — The ID of the run to cancel.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  status: string | null;
  previous_status: string | null;
}
```

</details>


<details>
<summary><code>delete_run</code> — DESTRUCTIVE — Permanently deletes an existing agent run</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes an existing agent run. This action is irreversible — the run record and all associated data will be permanently removed. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `id` (str, required) — The ID of the run to delete.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  deleted: boolean | null;
}
```

</details>


<details>
<summary><code>list_run_events</code> — Retrieves a list of events for a specific agent run</summary>

Retrieves a list of events for a specific agent run. Returns chronological events including steps, tool calls, and results. Use to monitor run progress or inspect what the agent did.

**Inputs:**
```
- `id` (str, required) — The ID of the run to get events for.
- `limit` (int, optional, default: 50) — Maximum events to return (1–200).
- `offset` (int, optional, default: 0) — Pagination offset.
```

**Output `data` schema:**

```typescript
{
  events: {
    id: string | null;
    type: string | null;
    created_at: string | null;
    data: Record<string, any> | null;
  }[];
  total: number | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "{ERROR_CODE}", "message": "{description}", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `limit` — Maximum number of items to return per page (varies per tool, typically 1–100)
- `offset` — Pagination offset for listing endpoints

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Run ID:**

```
UUID format string
Example: "run_abc123def456"
```

**Date/Time:**

```
ISO 8601 format string
Example: "2026-07-31T12:00:00Z"
```

</details>



## Getting Your Exa API Key

<details>
<summary><strong>Steps</strong></summary>

1. Go to [Exa Dashboard](https://dashboard.exa.ai)
2. Navigate to API Keys section
3. Click **Create API Key**
4. Copy the generated key — you will only see it once

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `x-api-key: YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your Exa request limits
- **Solution:**
  1. Check credit usage in your Exa dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact Exa support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Exa credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Exa API key
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `mewcp-exa/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Exa API Error</strong></summary>

- **Cause:** Upstream Exa API returned an error
- **Solution:**
  1. Check Exa service status at [Exa Status Page](https://status.exa.ai)
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Exa API Documentation](https://exa.ai/docs)** — Official API reference
- **[Exa API Reference](https://exa.ai/docs/reference)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>