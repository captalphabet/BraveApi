import asyncio

import pytest

from lib import BraveClient, BraveApiError
from httpobjects import WebSearchRequest, WebSearchApiResponse, Summarizer


class DummyResponse:
    """Stand-in for aiohttp.ClientResponse supporting async context manager."""

    def __init__(self, status: int, json_data: dict):
        self.status = status
        self._json_data = json_data
        self.url = "dummy://"

    async def json(self) -> dict:
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class DummySession:
    """Stand-in for aiohttp.ClientSession allowing controlled responses."""

    def __init__(self, response: DummyResponse):
        self._response = response
        self.requests: list[tuple] = []

    def get(self, url: str, params: dict | None = None, headers: dict | None = None):
        self.requests.append((url, params, headers))
        return self._response

    async def close(self):
        pass


class DummyLimiter:
    """No-op limiter for testing."""

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass


def test_web_search_success():
    dummy_json = {"type": "search", "query": {"original": "test"}}
    dummy_resp = DummyResponse(200, dummy_json)
    session = DummySession(dummy_resp)
    limiter = DummyLimiter()
    client = BraveClient(api_key="test-key", session=session, limiter=limiter)
    request = WebSearchRequest(q="test-query")
    response = asyncio.run(client.web_search(request))
    assert isinstance(response, WebSearchApiResponse)
    assert response.type == "search"
    assert session.requests[0][0] == client._api_path["web"]
    assert session.requests[0][1]["q"] == "test-query"


def test_web_search_error():
    dummy_json = {"error": "bad key"}
    dummy_resp = DummyResponse(401, dummy_json)
    session = DummySession(dummy_resp)
    limiter = DummyLimiter()
    client = BraveClient(api_key="test-key", session=session, limiter=limiter)
    with pytest.raises(BraveApiError) as exc:
        asyncio.run(client.web_search(WebSearchRequest(q="test")))
    assert exc.value.status == 401
    assert exc.value.data == dummy_json


def test_summarizer_search_success():
    dummy_json = {"summary": "This is a summary"}
    dummy_resp = DummyResponse(200, dummy_json)
    session = DummySession(dummy_resp)
    limiter = DummyLimiter()
    client = BraveClient(api_key="test-key", session=session, limiter=limiter)
    response = asyncio.run(client.summarizer_search("summary-key", entity_info=True))
    assert isinstance(response, Summarizer)


def test_summarizer_search_error():
    dummy_json = {"error": "forbidden"}
    dummy_resp = DummyResponse(403, dummy_json)
    session = DummySession(dummy_resp)
    limiter = DummyLimiter()
    client = BraveClient(api_key="test-key", session=session, limiter=limiter)
    with pytest.raises(BraveApiError) as exc:
        asyncio.run(client.summarizer_search("summary-key", entity_info=False))
    assert exc.value.status == 403
    assert exc.value.data == dummy_json

def test_web_search_bool_params_conversion():
    # Ensure boolean query parameters are converted to integers and defaults excluded
    dummy_json = {"type": "search", "query": {"original": "bool-test"}}
    dummy_resp = DummyResponse(200, dummy_json)
    session = DummySession(dummy_resp)
    limiter = DummyLimiter()
    client = BraveClient(api_key="test-key", session=session, limiter=limiter)
    # Set various boolean flags to test conversion and exclusion of defaults
    request = WebSearchRequest(
        q="bool-test", extra_snippets=True, spellcheck=False, summary=True
    )
    response = asyncio.run(client.web_search(request))
    assert isinstance(response, WebSearchApiResponse)
    params = session.requests[0][1]
    assert params.get("extra_snippets") == 1
    assert params.get("spellcheck") == 0
    assert params.get("summary") == 1
