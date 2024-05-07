from typing import List, Literal

from bs4 import BeautifulSoup

from .typed import Document


class WatercrawlTransformer:

    def __init__(self):
        try:
            import html2text
        except ImportError:
            raise ImportError(
                "Html2text is required for WatercrawlTransformer. "
                "Please install it with `pip install html2text`."
            )

    def transform(self, text: str, _format: Literal["markdown", "text"] = "markdown") -> str:
        if _format == "markdown":
            return self.to_markdown(text)
        if _format == "text":
            return self.to_content(text)

    def transform_documents(self,
                            documents: List[Document],
                            _format: Literal["markdown", "text"] = "markdown") -> List[Document]:
        docs = []
        for document in documents:
            transformed = self.transform(document.page_content, _format)
            doc = Document(transformed, document.metadata)
            docs.append(doc)
        return docs

    @staticmethod
    def to_content(html: str = "") -> str:
        if not isinstance(html, str):
            raise TypeError("html must be a string")
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.text.strip()
        return content

    @staticmethod
    def to_markdown(html: str = "") -> str:
        if not isinstance(html, str):
            raise TypeError("html must be a string")
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        content = h.handle(html)
        return content
