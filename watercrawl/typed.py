class Document:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata

    def __repr__(self):
        return "Document(page_content={}, metadata={})".format(
            self.page_content.replace("\n", "\\n"), str(self.metadata))

    def __str__(self):
        return "Document(page_content={}, metadata={})".format(
            self.page_content.replace("\n", "\\n"), str(self.metadata))
