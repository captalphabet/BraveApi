import asyncio
from aiohttp import web

import pytest

from lib import BraveClient
from httpobjects import WebSearchRequest, WebSearchApiResponse, Summarizer


def test_web_search_integration():
    async def go():
        async def handler(request):
            assert request.query.get("q") == "integration"
            return web.json_response({"type": "search", "query": {"original": "integration"}})

        app = web.Application()
        app.router.add_get("/res/v1/web/search", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]
        api_host = f"http://localhost:{port}"
        client = BraveClient(api_key="test-key", api_host=api_host)
        try:
            response = await client.web_search(WebSearchRequest(q="integration"))
        finally:
            await client.close()
            await runner.cleanup()
        return response

    response = asyncio.run(go())
    assert isinstance(response, WebSearchApiResponse)
    assert response.query.original == "integration"


def test_summarizer_search_integration():
    async def go():
        async def handler(request):
            assert request.query.get("key") == "abc"
            assert request.query.get("entity_info") == "1"
            return web.json_response({"summary": "test"})

        app = web.Application()
        app.router.add_get("/res/v1/summarizer/search", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]
        api_host = f"http://localhost:{port}"
        client = BraveClient(api_key="test-key", api_host=api_host)
        try:
            response = await client.summarizer_search("abc", entity_info=True)
        finally:
            await client.close()
            await runner.cleanup()
        return response

    response = asyncio.run(go())
    assert isinstance(response, Summarizer)