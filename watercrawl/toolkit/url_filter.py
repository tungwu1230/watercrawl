from typing import List

from urllib.parse import urljoin, urlparse


def get_base_url(url: str) -> str:
    u = urlparse(url)
    return u.scheme + "://" + u.hostname


def remove_duplicates(urls: List[str]) -> List[str]:
    return list(dict.fromkeys(urls))


def remove_invalid_urls(urls: List[str]) -> List[str]:
    return [url for url in urls if url.startswith("https://") or url.startswith("http://")]


def absolute_urls(base_url: str, urls: List[str]) -> List[str]:
    return [urljoin(base_url, url, allow_fragments=False) for url in urls]


def remain_same_domain_urls(base_url, urls: List[str]) -> List[str]:
    return [url for url in urls if base_url in url]


def excludes_urls(urls: List[str], excludes: str) -> List[str]:
    pass


def includes_urls(urls: List[str], excludes: str) -> List[str]:
    pass
