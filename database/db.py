import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                email   TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS items (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                canonical_name  TEXT NOT NULL UNIQUE,
                category        TEXT,
                mount           TEXT,
                created_at      TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS aliases (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL REFERENCES items(id),
                alias   TEXT NOT NULL UNIQUE
            );

            CREATE INDEX IF NOT EXISTS idx_aliases_alias ON aliases(alias);

            CREATE TABLE IF NOT EXISTS posts (
                post_id         TEXT PRIMARY KEY,
                subreddit       TEXT NOT NULL,
                title           TEXT NOT NULL,
                url             TEXT NOT NULL,
                author          TEXT,
                listing_type    TEXT CHECK(listing_type IN ('WTS', 'WTB', 'WTT')),
                seen_at         TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS price_history (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id         INTEGER NOT NULL REFERENCES items(id),
                post_id         TEXT NOT NULL REFERENCES posts(post_id),
                price           REAL,
                raw_price_text  TEXT,
                condition       TEXT,
                seen_at         TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS watchlist (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER REFERENCES users(id),
                item_id     INTEGER REFERENCES items(id),
                category    TEXT,
                mount       TEXT,
                max_price   REAL
            );
        """)
    conn.close()
