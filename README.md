# braveapi

A lightweight asynchronous Python client for the Brave Search API.

## Features

- Pydantic models for request/response validation
- Asynchronous HTTP requests via aiohttp
- Rate limiting via aiolimiter
- Rich terminal logging via rich

## Installation

Install from PyPI:

```bash
pip install braveapi
```

Or install locally (and for development):

```bash
pip install .
pip install .[dev]
```

## Configuration

Set your Brave Search subscription key as an environment variable:

```bash
export BRAVE_API_KEY=<your_api_key>
```

## Project layout

Key files and directories:

```
.
├── lib.py                # BraveClient implementation
├── httpobjects.py        # Pydantic request/response models
├── main.py               # Example/CLI usage script
├── tests/                # Unit tests (pytest)
├── docs/                 # API specs and parsing utilities
├── AGENTS.md             # Agent workstream guide
├── README.md             # This file
├── pyproject.toml        # Package metadata & dependencies
└── uv.lock               # Locked dependency versions
```

## Quickstart

```python
import asyncio
from lib import BraveClient, BraveApiError
from httpobjects import WebSearchRequest, WebSearchApiResponse

async def main():
    # Initialize client (api_key via BRAVE_API_KEY env var by default)
    async with BraveClient(api_key=None) as client:
        try:
            req = WebSearchRequest(q="openai")
            resp: WebSearchApiResponse = await client.web_search(req)
            print(resp)
        except BraveApiError as exc:
            print(f"Web search error {exc.status}: {exc.data}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Summarizer example

```python
import asyncio
from lib import BraveClient, BraveApiError

async def summarize(key: str):
    async with BraveClient() as client:
        try:
            summary = await client.summarizer_search(key, entity_info=True)
            print(summary)
        except BraveApiError as exc:
            print(f"Summarizer error {exc.status}: {exc.data}")

if __name__ == "__main__":
    # replace 'your-summary-key' with a key obtained from web_search(summary=True)
    asyncio.run(summarize('your-summary-key'))
```

## Running tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please open issues and pull requests.

## Advanced topics

- **Spec → model generation**: See `docs/utils/parse_html_docs.py` and `docs/parse_html_docs.md` for how to extract API model definitions from the raw HTML docs.
- **Agent tasks**: For agent-based workstream breakdown, see [AGENTS.md](AGENTS.md).
