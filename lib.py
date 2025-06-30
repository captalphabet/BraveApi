import logging
import os
# Utilities for URL handling
from urllib.parse import urljoin

try:
    from aiohttp import ClientSession, ClientTimeout, TCPConnector
except ImportError:
    ClientSession = None
    ClientTimeout = None
    TCPConnector = None

try:
    from aiolimiter import AsyncLimiter
except ImportError:
    class AsyncLimiter:
        """No-op async limiter when aiolimiter is not installed."""

        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            pass

        async def __aexit__(self, exc_type, exc, tb):
            pass

from httpobjects import WebSearchRequest, WebSearchApiResponse, Summarizer




API_HOST = "https://api.search.brave.com"


class BraveApiError(Exception):
    """Exception raised when the Brave API returns a non-200 response."""

    def __init__(self, status: int, data: dict):
        super().__init__(f"Brave API returned status {status}")
        self.status = status
        self.data = data


class BraveClient:
    """Asynchronous client for interacting with the Brave Search API."""

    def __init__(
        self,
        api_key: str | None = None,
        api_host: str | None = None,
        max_concurrent_requests: int = 1,
        rps: int = 1,
        timeout: int = 20,
        session: ClientSession | None = None,
        limiter: AsyncLimiter | None = None,
    ) -> None:
        self._api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self._api_key:
            raise ValueError("BRAVE_API_KEY must be provided via api_key or environment variable")

        self._api_host = api_host or API_HOST
        self._api_path = {
            "web": urljoin(self._api_host, "res/v1/web/search"),
            "summarizer": urljoin(self._api_host, "res/v1/summarizer/search"),
        }
        self._headers = {
            "web": {"X-Subscription-Token": self._api_key, "Api-Version": "2023-10-11"},
            "summarizer": {"X-Subscription-Token": self._api_key, "Api-Version": "2024-04-23"},
        }

        self._session = session
        self._max_concurrent_requests = max_concurrent_requests
        self._timeout_seconds = timeout
        self._limiter = limiter or AsyncLimiter(rps, 1)

    async def _ensure_session(self) -> None:
        """Lazily initialize the HTTP session in an async context."""
        if self._session is None:
            self._session = ClientSession(
                connector=TCPConnector(limit=self._max_concurrent_requests),
                timeout=ClientTimeout(self._timeout_seconds),
            )

    async def web_search(self, request: WebSearchRequest) -> WebSearchApiResponse:
        """Perform a web search query and return a parsed WebSearchApiResponse."""
        await self._ensure_session()
        # Exclude unset (None) and default fields to avoid unwanted boolean/query params
        params = request.model_dump(exclude_none=True, exclude_defaults=True)
        for key, value in list(params.items()):
            if isinstance(value, bool):
                params[key] = int(value)
        async with self._limiter:
            async with self._session.get(
                self._api_path["web"], params=params, headers=self._headers["web"]
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    raise BraveApiError(resp.status, data)
                return WebSearchApiResponse.model_validate(data)

    async def summarizer_search(
        self, key: str, entity_info: bool = False
    ) -> Summarizer:
        """Fetch a summary using a summary key from a previous web search."""
        await self._ensure_session()
        params: dict[str, int | str] = {"key": key}
        if entity_info:
            params["entity_info"] = 1

        async with self._limiter:
            async with self._session.get(
                self._api_path["summarizer"], params=params, headers=self._headers["summarizer"]
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    raise BraveApiError(resp.status, data)
                return Summarizer.model_validate(data)

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
