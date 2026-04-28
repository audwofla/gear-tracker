from matching.normalizer import normalize

_BUNDLE_SIGNALS = {"+", "kit", "bundle", "lot", "&"}


def match_post(title: str, alias_map: dict[frozenset, int]) -> list[int]:
    """
    Returns a list of matched item_ids.
    - 0 items → Claude fallback needed
    - 1 item  → single match (try regex for price first)
    - 2+ items → bundle, Claude assigns prices per item
    """
    title_tokens = normalize(title)
    return [item_id for tokens, item_id in alias_map.items() if tokens <= title_tokens]


def is_bundle(title: str, matched_ids: list[int]) -> bool:
    """True if the post looks like a bundle listing."""
    title_tokens = normalize(title)
    return len(matched_ids) >= 2 or bool(title_tokens & _BUNDLE_SIGNALS)
