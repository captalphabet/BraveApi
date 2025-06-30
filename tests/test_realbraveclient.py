from lib import BraveClient, BraveApiError
from httpobjects import WebSearchApiResponse, WebSearchRequest
import asyncio
import pytest



def test_real_query():
    loop  = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = BraveClient()
    requestob = WebSearchRequest(q="What was the controversy concering the supreme court in the us")
    response = asyncio.run(client.web_search(requestob))
    loop.close()
    assert isinstance(response,WebSearchApiResponse)
    print(response.model_dump_json(indent=2))


















