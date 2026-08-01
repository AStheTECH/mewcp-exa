---
type: Auth
title: Authentication
description: How the server authenticates upstream Exa requests.
resource: https://exa.ai/docs/reference/search-api-guide-for-coding-agents
timestamp: 2026-07-29T19:18:56Z
---

## Authentication

All requests require an API key in this header:
  x-api-key: <api_key>

*(Note: The API also accepts `Authorization: Bearer <api_key>`)*

Required credential fields:
- `api_key` (secret) — The Exa API key

**API base URL:** https://api.exa.ai