from matching.normalizer import normalize


def load_alias_map(conn) -> dict[frozenset, int]:
    """Load all aliases from DB into a frozenset(tokens) -> item_id map."""
    with conn.cursor() as cur:
        cur.execute("SELECT alias, item_id FROM aliases")
        return {normalize(alias): item_id for alias, item_id in cur.fetchall()}
