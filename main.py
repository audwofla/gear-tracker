import logging
import time

from database.db import init_db
from database.posts import insert_posts
from reddit.scraper import poll_subreddits

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

POLL_INTERVAL = 60  # seconds


def run():
    init_db()
    logger.info("Starting poll loop (interval=%ds)", POLL_INTERVAL)

    while True:
        try:
            posts = poll_subreddits()
            new_count = insert_posts(posts)
            logger.info("Inserted %d new posts", new_count)
        except Exception:
            logger.exception("Error during poll cycle")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
