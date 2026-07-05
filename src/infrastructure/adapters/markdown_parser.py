import markdown  # type: ignore
from typing import List, Optional

class MarkdownParser:
    def __init__(self, extensions: Optional[List[str]] = None) -> None:
        self.extensions = extensions or ["fenced_code", "tables"]

    def to_html(self, text: str) -> str:
        if not text:
            return ""
        return markdown.markdown(text, extensions=self.extensions)
