import re

_PUNCT_RE = re.compile(r"[^\w\s]")


def normalize(text: str) -> frozenset[str]:
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    return frozenset(text.split())
