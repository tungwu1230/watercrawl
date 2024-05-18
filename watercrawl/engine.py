import asyncio
import logging
from typing import Iterable, List, Literal

from tqdm import tqdm

from .config import default_header_template
from .typed import Document

logger = logging.getLogger(__name__)


class WatercrawlEngine:

    def __init__(self, engine: Literal["requests", "playwright"] = "requests"):
        self.engine = engine

    def run(self, urls: List[str]) -> List[Document]:
        if self.engine == "requests":
            return list(self.run_requests(urls))
        if self.engine == "playwright":
            return list(self.run_playwright(urls))

    @staticmethod
    def run_requests(urls: List[str]) -> Iterable[Document]:
        for url in tqdm(urls):
            resp = scrape_with_requests(url)
            yield Document(page_content=resp,
                           metadata={"source": url})

    @staticmethod
    def run_playwright(urls: List[str]) -> Iterable[Document]:
        for url in tqdm(urls):
            resp = asyncio.run(ascrape_with_playwright(url))
            yield Document(page_content=resp,
                           metadata={"source": url})


def scrape_with_requests(url: str) -> str:
    """Scrape a URL with `requests`."""
    import requests
    res = requests.get(url, headers=default_header_template)
    return res.text


def route_intercept(route):
    if route.request.resource_type == "image":
        # print(f"Blocking the image request to: {route.request.url}")
        return route.abort()
    if "google" in route.request.url:
        # print(f"blocking {route.request.url} as it contains Google")
        return route.abort()
    return route.continue_()


async def ascrape_with_playwright(url: str, headless: bool = True) -> str:
    """Scrape a URL with playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise ImportError(
            "playwright is required when using `ascrape_with_playwright()`. "
            "Please install it with `pip install playwright`."
        )

    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        try:
            page = await browser.new_page()
            await page.route("**/*", route_intercept)  # Intercept all requests
            await page.goto(url)
            results = await page.content()  # Simply get the HTML content
            logger.info("Content scraped")
        except Exception as e:
            logger.info(f"Error: {e}")
        await browser.close()
    return results
