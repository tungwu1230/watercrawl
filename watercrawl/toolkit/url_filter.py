import fnmatch
import re
from typing import List

from urllib.parse import urljoin, urlparse


def get_base_url(url: str) -> str:
    u = urlparse(url)
    return u.scheme + "://" + u.hostname


def remove_duplicates(urls: List[str]) -> List[str]:
    no_duplicates = list(dict.fromkeys(urls))
    no_duplicates.sort()
    return no_duplicates


def remove_invalid_urls(urls: List[str]) -> List[str]:
    return [url for url in urls if url.startswith("https://") or url.startswith("http://")]


def absolute_urls(base_url: str, urls: List[str]) -> List[str]:
    return [urljoin(base_url, url, allow_fragments=False) for url in filter(lambda url: isinstance(url, str), urls)]


def remain_same_domain_urls(base_url, urls: List[str]) -> List[str]:
    return [url for url in urls if base_url in url]


def includes_urls(urls: List[str], pattern: str) -> List[str]:
    regex = fnmatch.translate(pattern)
    pattern = re.compile(regex)
    return [url for url in filter(lambda url: isinstance(url, str), urls) if pattern.match(urlparse(url).path)]


def excludes_urls(urls: List[str], pattern: str) -> List[str]:
    regex = fnmatch.translate(pattern)
    pattern = re.compile(regex)
    return [url for url in filter(lambda url: isinstance(url, str), urls) if not pattern.match(urlparse(url).path)]
