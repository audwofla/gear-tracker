from database.db import get_connection


def insert_post(post: dict) -> bool:
    """Insert a post. Returns True if inserted, False if already seen."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO posts (post_id, subreddit, title, body, url, author, listing_type)
                VALUES (%(post_id)s, %(subreddit)s, %(title)s, %(body)s, %(url)s, %(author)s, %(listing_type)s)
                ON CONFLICT (post_id) DO NOTHING
                """,
                post,
            )
            return cur.rowcount == 1


def insert_posts(posts: list[dict]) -> int:
    """Insert a list of posts. Returns count of newly inserted posts."""
    return sum(insert_post(p) for p in posts)
