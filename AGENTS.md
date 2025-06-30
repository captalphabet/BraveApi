# Agent’s Guide to BraveApi

Below is a high‑level “tour” of the BraveApi project as it stands today: its purpose, goals, current state, key modules, documentation/specs, and the Python‑level dependencies and tooling in use.

---

## 1. Project identity & metadata

```toml
[project]
name = "braveapi"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "aiohttp>=3.12.13",
    "aiolimiter>=1.2.1",
    "pydantic>=2.11.7",
    "rich>=14.0.0",
]
```

```text
# specify Python interpreter version (pyenv/asdf)
3.12
```

---

## 2. Purpose & goals

**Purpose**
- This is a lightweight, asynchronous Python client for Brave Search’s public HTTP API. It aims to encapsulate the Brave Search endpoints, validate requests and responses via Pydantic, handle rate limiting and concurrency, and provide a solid foundation for integration.

**Goals**
- Fully flesh out response model schemas based on the official specs.
- Automate generation of Pydantic models from the HTML docs.
- Offer clear documentation and examples for Python users.

---

## 3. Current implementation state

### Core client (`lib.py`)
- Defines `BraveClient` and `BraveApiError` for error handling.
- Implements `web_search()` and `summarizer_search()` using aiohttp and aiolimiter.

```python
class BraveApiError(Exception):
    """Exception raised when the Brave API returns a non-200 response."""
    def __init__(self, status: int, data: dict):
        super().__init__(f"Brave API returned status {status}")
        self.status = status
        self.data = data

class BraveClient:
    """Asynchronous client for interacting with the Brave Search API."""
    # init sets up API key, host, paths, headers, session, limiter

    async def web_search(self, request: WebSearchRequest) -> WebSearchApiResponse:
        params = request.model_dump(exclude_none=True)
        async with self._limiter:
            async with self._session.get(self._api_path['web'], params=params, headers=self._headers['web']) as resp:
                data = await resp.json()
                if resp.status != 200:
                    raise BraveApiError(resp.status, data)
                return WebSearchApiResponse.model_validate(data)
```

### Pydantic models (`httpobjects.py`)
- `WebSearchRequest` fully describes query parameters.
- Response submodels are currently stubs and need filling from the specs.

```python
class WebSearchRequest(BaseModel):
    q: str
    country: str = "US"
    count: Optional[int] = 20
    extra_snippets: Optional[bool] = False
    freshness: Optional[str] = None
    goggles: Optional[List[str]] = None
    offset: Optional[int] = 0
    result_filter: Optional[str] = None
    safesearch: Optional[str] = "moderate"
    search_lang: str = "en"
    spellcheck: Optional[bool] = True
    summary: Optional[bool] = None
    text_decorations: Optional[bool] = True
    ui_lang: str = "en-US"
    units: Optional[str] = None

# response-side stubs:
class DiscussionResult(BaseModel):
    pass
```

---

## 4. Documentation & specs

All schema specs live under `docs/`:

| File                    | Purpose                                      |
|-------------------------|----------------------------------------------|
| WebRequestSpec.md       | TypeScript interface for web search request  |
| parse_html_docs.md      | Recipe for parsing HTML docs to JSON schemas |
| WebResponseSpec.md      | Markdown tables of WebSearchApiResponse spec |
| ResponseDocsMk2.md      | Working draft of response spec               |
| ResponseSpecFinal.md    | Consolidated API review document             |

---

## 5. Spec scraping helper (`docs/utils/parse_html_docs.py`)

Uses BeautifulSoup to extract `<section id=...>` model tables from raw HTML:

```python
from bs4 import BeautifulSoup
# parse sections and write out trimmed HTML
```

---

## 6. Testing & development tooling

- **pytest** with simple async tests in `tests/`
- `Argcfile.sh` for running tests inside the virtualenv via argc
- robust logging with logging module and RichHandler()

```bash
# @cmd test and source env
testProj () {
  source ".venv/bin/activate"
  pytest
}
```

---

## 7. Locked dependencies (`uv.lock`)

```toml
version = 1
revision = 1
requires-python = ">=3.12"
```

---

## 8. Summary of tools & dependencies

| Category             | Tool / Library        |
|----------------------|-----------------------|
| HTTP client          | aiohttp ≥ 3.12.13     |
| Rate limiting        | aiolimiter ≥ 1.2.1    |
| Data validation      | pydantic ≥ 2.11.7     |
| Logging/UI           | rich ≥ 14.0.0         |
| Testing              | pytest + asyncio      |
| Spec parsing         | beautifulsoup4        |
| CLI dev script       | argc                  |
| Lock file            | uv.lock               |
| Python version       | 3.12                  |

---

### Next steps
- Fill out all response submodels using the Markdown/HTML specs.
- Flesh out README.md with usage and examples.
- Automate spec → model generation as part of the build.
- Add CI and packaging pipeline.

---

## 9. Parallel tasks for agents
- ### Task assignments for simultaneous work on separate branches
- **agent-1**: Response model completion – populate remaining response submodels in `httpobjects.py`.
- **agent-2**: Model generator – build/refine script that transforms HTML specs to Pydantic classes.

- **✅ Completed tasks**
  - Integration tests (tests/test_integration_braveclient.py)
  - Unit tests for boolean parameter conversion (tests/test_client.py)
  - Scaffold DiscussionResult & ForumData models and unit tests (httpobjects.py, tests/test_dataobjs.py)

- **Pending tasks**
  - Response model completion: Populate remaining response submodels in `httpobjects.py`.
  - Model generator: Build/refine script that transforms HTML specs to Pydantic classes.
  - README & examples: Expand `README.md` with installation instructions and examples.
  - CI/CD setup: Configure continuous integration and automated package publishing.
  - Packaging & release: Add build/publish configuration, version bump flow, and PyPI metadata.
  - Linting & typing: Integrate linter (ruff), formatter (black), and type checker (pyright).
  - Performance benchmarks: Measure request throughput and rate-limit performance.


# Expected Behaviour

After finishing a task append a log summary of the diff to the .agent_log.md file
Multiple agents can be running in parallel
