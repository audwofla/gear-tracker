import psycopg2
import psycopg2.extras
from config import DB_DSN


def get_connection():
    conn = psycopg2.connect(DB_DSN)
    return conn


def init_db():
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id      SERIAL PRIMARY KEY,
                    email   TEXT NOT NULL UNIQUE
                );

                CREATE TABLE IF NOT EXISTS items (
                    id              SERIAL PRIMARY KEY,
                    canonical_name  TEXT NOT NULL UNIQUE,
                    category        TEXT,
                    mount           TEXT,
                    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS aliases (
                    id      SERIAL PRIMARY KEY,
                    item_id INTEGER NOT NULL REFERENCES items(id),
                    alias   TEXT NOT NULL UNIQUE
                );

                CREATE INDEX IF NOT EXISTS idx_aliases_alias ON aliases(alias);

                CREATE TABLE IF NOT EXISTS posts (
                    post_id         TEXT PRIMARY KEY,
                    subreddit       TEXT NOT NULL,
                    title           TEXT NOT NULL,
                    body            TEXT,
                    url             TEXT NOT NULL,
                    author          TEXT,
                    listing_type    TEXT CHECK(listing_type IN ('WTS', 'WTB', 'WTT')),
                    seen_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS price_history (
                    id              SERIAL PRIMARY KEY,
                    item_id         INTEGER NOT NULL REFERENCES items(id),
                    post_id         TEXT NOT NULL REFERENCES posts(post_id),
                    price           NUMERIC,
                    raw_price_text  TEXT,
                    condition       TEXT,
                    seen_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );

                CREATE TABLE IF NOT EXISTS watchlist (
                    id          SERIAL PRIMARY KEY,
                    user_id     INTEGER REFERENCES users(id),
                    item_id     INTEGER REFERENCES items(id),
                    category    TEXT,
                    mount       TEXT,
                    max_price   NUMERIC
                );

                CREATE TABLE IF NOT EXISTS keywords (
                    id      SERIAL PRIMARY KEY,
                    keyword TEXT NOT NULL UNIQUE
                );
            """)
    conn.close()
