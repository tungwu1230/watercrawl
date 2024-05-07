from watercrawl import WatercrawlApp

url = 'https://example.com'
app = WatercrawlApp(engine="requests")
content = app.scrape(url)
print(content)

urls = ['https://example.com']
app = WatercrawlApp(engine="playwright")
docs = app.scrape_urls(urls)
print(docs)

start_url = 'https://example.com'
app = WatercrawlApp(engine="playwright")
docs = app.crawl(start_url, limit=10)
print(docs)
