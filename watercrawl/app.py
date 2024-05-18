import logging
from typing import Literal, Optional

from .engine import WatercrawlEngine
from .extractor import WatercrawlExtractor, extract_links
from .toolkit.url_filter import *
from .transformer import WatercrawlTransformer
from .typed import Document

logger = logging.getLogger(__name__)


class WatercrawlApp:

    def __init__(self, engine: Literal["requests", "playwright"] = "requests") -> None:
        self.engine = WatercrawlEngine(engine)
        self.extractor = WatercrawlExtractor()
        self.transformer = WatercrawlTransformer()

    def scrape(self, url: str, only_main_content: bool = True, to_markdown: bool = True) -> Document:
        docs = self.engine.run([url])
        docs = self.extractor.extract_documents(docs, "metadata")
        if only_main_content:
            docs = self.extractor.extract_documents(docs, "main_content")
        if to_markdown:
            transform_format: Literal["markdown", "text"] = "markdown"
        else:
            transform_format: Literal["markdown", "text"] = "text"
        transformed = self.transformer.transform_documents(docs, transform_format)
        return transformed[0]

    def scrape_urls(self, urls: List[str], only_main_content: bool = True, to_markdown: bool = True) -> List[Document]:
        """Scrape multiple URLs."""
        docs = self.engine.run(urls)
        docs = self.extractor.extract_documents(docs, "metadata")
        if only_main_content:
            docs = self.extractor.extract_documents(docs, "main_content")
        if to_markdown:
            transform_format: Literal["markdown", "text"] = "markdown"
        else:
            transform_format: Literal["markdown", "text"] = "text"
        transformed = self.transformer.transform_documents(docs, transform_format)
        return transformed

    def crawl(self, start_url: str, limit: int = 10,
              only_main_content: bool = True, to_markdown: bool = True,
              include_rule: Optional[str] = None, exclude_rule: Optional[str] = None) -> List[Document]:
        """Autocrawl """
        start_doc = self.engine.run([start_url])[0]
        html = start_doc.page_content

        base_url = get_base_url(start_url)
        page_links = extract_links(html)

        urls = absolute_urls(base_url, page_links)
        urls = remove_duplicates(urls)
        urls = remove_invalid_urls(urls)
        urls = remain_same_domain_urls(base_url, urls)

        if include_rule:
            urls = includes_urls(urls, include_rule)

        if exclude_rule:
            urls = excludes_urls(urls, exclude_rule)

        docs = self.engine.run(urls[:limit])
        docs = [start_doc] + docs

        docs = self.extractor.extract_documents(docs, "metadata")

        if only_main_content:
            docs = self.extractor.extract_documents(docs, "main_content")
        if to_markdown:
            transform_format: Literal["markdown", "text"] = "markdown"
        else:
            transform_format: Literal["markdown", "text"] = "text"

        transformed = self.transformer.transform_documents(docs, transform_format)
        return transformed
