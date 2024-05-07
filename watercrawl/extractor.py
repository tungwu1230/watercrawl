import logging
from typing import Dict, List, Literal

from bs4 import BeautifulSoup

from .typed import Document

logger = logging.getLogger(__name__)


class WatercrawlExtractor:

    def __init__(self):
        pass

    @staticmethod
    def extract_documents(
            documents: List[Document],
            method: Literal["main_content", "metadata"] = "main_content") -> List[Document]:
        if method == "main_content":
            for document in documents:
                document.page_content = extract_main_content(document.page_content)
            return documents
        if method == "metadata":
            for document in documents:
                document.metadata.update(extract_metadata(document.page_content))
            return documents


def extract_metadata(html: str) -> Dict:
    """Extract metadata from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    metadata = {}
    title = soup.find("title")
    title = title.string.strip() if title else ""

    description = soup.find("meta", attrs={"name": "description"})
    description = description.attrs["content"] if description else ""

    keywords = soup.find("meta", attrs={"name": "keywords"})
    keywords = keywords.attrs["content"] if keywords else ""

    metadata.update({"title": title, "description": description, "keywords": keywords})
    return metadata


def extract_links(html: str) -> List[str]:
    """Extract links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        links.append(href)
    return links


def extract_main_content(html: str) -> str:
    """Extract main content from HTML.\n
    Remove <script> and <style> tags.\n
    Remove <header>, <nav>, <footer> tags.\n
    Remove <a> and <img> tags
    """
    soup = BeautifulSoup(html, "html.parser")
    cleaned_content = remove_unwanted_tags(
        str(soup.body), unwanted_tags=["script", "style", "header", "nav", "footer", "a", "img"])
    return cleaned_content


def remove_unwanted_tags(html: str, unwanted_tags: List[str]) -> str:
    """Remove unwanted tags from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()
    return str(soup)
