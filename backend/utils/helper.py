# backend/utils/helper.py
import re

def safe_text(text: str, max_len: int = 900) -> str:
    """
    Clean some HTML/snippets from DuckDuckGo and trim length.
    """
    if not isinstance(text, str):
        return ""
    # remove simple HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\n", " ").strip()
    if len(text) > max_len:
        text = text[: max_len - 3] + "..."
    return text
