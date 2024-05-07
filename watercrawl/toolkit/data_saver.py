import os
from typing import List, Literal, Optional
from uuid import uuid4
from urllib.parse import urlparse


from ..typed import Document


def save_documents(documents: List[Document],
                   output_path: Optional[str] = None,
                   strategy: Literal["website_structure", "uuid"] = "uuid") -> None:
    """Save documents to current working directory or specifical output directory."""
    if not output_path:
        output_path = os.path.join(os.getcwd(), "website" if strategy == "website_structure" else "output")

    os.makedirs(output_path, exist_ok=True)

    # TODO: Error
    if strategy == "website_structure":
        for document in documents:
            path = urlparse(document.metadata["source"]).path
            if path == "" or path == "/":
                path = ""
            # print(os.path.join(output_path, path))
            os.makedirs(os.path.join(output_path, path), exist_ok=True)
            with open(os.path.join(output_path, path, "index.md"), "w") as f:
                f.write(document.page_content)
    else:
        for document in documents:
            with open(os.path.join(output_path, f"{uuid4()}.md"), "w") as f:
                f.write(document.page_content)

    print(f"Saved {len(documents)} documents to {output_path}")
