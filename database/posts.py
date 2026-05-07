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


def get_unprocessed_posts(conn) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT post_id, subreddit, title, body, url, author, listing_type"
            " FROM posts WHERE processed = FALSE ORDER BY seen_at"
        )
        cols = [d.name for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def mark_processed(conn, post_id: str) -> None:
    with conn.cursor() as cur:
        cur.execute("UPDATE posts SET processed = TRUE WHERE post_id = %s", (post_id,))
