# 💧Watercrawl

Crawl and convert any website into LLM-ready markdown.  
Build by tung.wu.1230

## What is watercrawl
Watercrawl is a tool for crawling website into LLM friendly format.

## Installation
Clone the repo and using the following command to install `watercrawl`.
```text
python setup.py install
```

## How to use it?

Example (scrape single page):
```python
from watercrawl import WatercrawlApp

url = 'https://example.com'
app = WatercrawlApp(engine="requests")
content = app.scrape(url)

print(content)
```

Output:
```text
Document(
    page_content=URL Source: https://example.com\n\nContent:\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n,
    metadata={
        "source": "https://example.com",
        "status": "ok",
        "title": "Example Domain",
        "description": "",
        "keywords": ""
    }
)
```

Example (scrape mutiple urls):
```python
from watercrawl import WatercrawlApp

urls = ['https://example.com']
app = WatercrawlApp(engine="playwright")
docs = app.scrape_urls(urls)
print(docs)
```

Output:
```text
[Document(page_content=URL Source: https://example.com\n\nContent:\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n, metadata={'source': 'https://example.com', 'title': 'Example Domain', 'description': '', 'keywords': ''})]
```

Example (auto crawl other links from a url):
```python
from watercrawl import WatercrawlApp

start_url = 'https://example.com'
app = WatercrawlApp(engine="playwright")
docs = app.crawl(start_url, limit=10)
print(docs)
```

```text
[Document(page_content=URL Source: https://example.com\n\nContent:\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n, metadata={'source': 'https://example.com', 'title': 'Example Domain', 'description': '', 'keywords': ''})]
```