"""SQLite access. One small file so every step can see exactly how data is stored."""
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("HUB_DB_PATH", "hub.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id        TEXT PRIMARY KEY,
    customer_email  TEXT NOT NULL,
    status          TEXT NOT NULL,      -- created | fulfilled | refunded
    total_cents     INTEGER,            -- money as integer cents, never floats
    tracking_number TEXT,
    updated_at      TEXT NOT NULL
);
"""


@contextmanager
def connect():
    """Open a connection, commit if all went well, always close it."""
    conn = sqlite3.connect(DB_PATH, timeout=2)
    conn.row_factory = sqlite3.Row  # rows behave like dicts: row["status"]
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
