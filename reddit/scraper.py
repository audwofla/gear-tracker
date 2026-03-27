import logging
import re
import time
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger(__name__)

_ATOM_NS = "http://www.w3.org/2005/Atom"
_NS = {"atom": _ATOM_NS}

SUBREDDIT = "photomarket"
DEFAULT_SUBREDDITS = ["photomarket"]

# Matches both [WTS]/[B] style and plain WTS/WTB/WTT
_LISTING_TYPE_RE = re.compile(r"\b\[?(WTS|WTB|WTT|S|B|T)\]?\b", re.IGNORECASE)
_LISTING_TYPE_MAP = {"S": "WTS", "B": "WTB", "T": "WTT"}


_USER_AGENT = "gear-tracker/0.1 (RSS ingest)"
_TIMEOUT = 15


def _parse_listing_type(title: str) -> str | None:
    m = _LISTING_TYPE_RE.search(title)
    if not m:
        return None
    val = m.group(1).upper()
    return _LISTING_TYPE_MAP.get(val, val)


def _post_id_from_atom_id(atom_id: str) -> str:
    atom_id = atom_id.strip()
    return atom_id[3:] if atom_id.startswith("t3_") else atom_id


def fetch_posts(subreddit: str, limit: int = 25) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/new/.rss?limit={limit}"
    logger.debug("Fetching r/%s (limit=%d)", subreddit, limit)

    resp = requests.get(url, headers={"User-Agent": _USER_AGENT}, timeout=_TIMEOUT)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", _NS)
    logger.info("r/%s: got %d entries", subreddit, len(entries))

    posts = []
    for entry in entries:
        def get(tag):
            el = entry.find(f"atom:{tag}", _NS)
            return el.text.strip() if el is not None and el.text else ""

        link_el = entry.find("atom:link", _NS)
        post_url = link_el.get("href", "") if link_el is not None else ""

        author_el = entry.find("atom:author/atom:name", _NS)
        author = author_el.text.strip() if author_el is not None and author_el.text else None

        title = get("title")
        post_id = _post_id_from_atom_id(get("id"))
        listing_type = _parse_listing_type(title)

        logger.debug("post=%s type=%s title=%r", post_id, listing_type, title)

        posts.append({
            "post_id": post_id,
            "subreddit": subreddit,
            "title": title,
            "url": post_url,
            "author": author,
            "listing_type": listing_type,
        })

    return posts


def poll_subreddits(
    subreddits: list[str] = DEFAULT_SUBREDDITS,
    delay_between: float = 2.0,
) -> list[dict]:
    all_posts = []
    for i, sub in enumerate(subreddits):
        if i > 0:
            time.sleep(delay_between)
        all_posts.extend(fetch_posts(sub))
    logger.info("Poll complete: %d total posts from %d subreddits", len(all_posts), len(subreddits))
    return all_posts


if __name__ == "__main__":
    posts = fetch_posts(SUBREDDIT)
    print(posts)