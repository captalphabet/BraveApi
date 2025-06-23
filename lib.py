import asyncio
import json
import logging
import os
from urllib.parse import urljoin
from rich.logging import RichHandler

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiolimiter import AsyncLimiter

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()]
)
log = logging.getLogger(__name__)



API_HOST = "https://api.search.brave.com"
API_PATH = {
    "web": urljoin(API_HOST, "res/v1/web/search"),
    "summarizer_search": urljoin(API_HOST, "res/v1/summarizer/search"),
}
try:
    API_KEY = os.getenv("BRAVE_API_KEY")
    log.info("Api key set")
except Exception as e:
    log.error("Api key not set")

# Create request headers for specific endpoints
API_HEADERS = {
    "web": {"X-Subscription-Token": API_KEY, "Api-Version": "2023-10-11"},
    "summarizer": {"X-Subscription-Token": API_KEY, "Api-Version": "2024-04-23"},
}
