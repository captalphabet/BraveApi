from lib import BraveClient,BraveApiError
from httpobjects import WebSearchRequest, WebSearchApiResponse
import asyncio

async def simple_search():
    client = BraveClient()

    query =  WebSearchRequest(q="How has trump affected the courts",summary=True)
    
    try:
        response = await client.web_search(query)
        if response.summarizer
        print(response.web.model_dump_json(indent=4))
        
    except BraveApiError as be:
        print("failed with: {be}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(simple_search())
    



