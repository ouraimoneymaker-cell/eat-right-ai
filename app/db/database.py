from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DEFAULT_DB_PATH = Path(os.getenv("EAT_RIGHT_DB_PATH", "storage/eat_right_ai.db"))


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DEFAULT_DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lookup_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                lookup_value TEXT NOT NULL,
                metadata_json TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                barcode TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def log_lookup_event(event_type: str, lookup_value: str, metadata_json: str | None = None) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO lookup_events (event_type, lookup_value, metadata_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (event_type, lookup_value, metadata_json, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_lookup_events(limit: int = 50) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT event_type, lookup_value, metadata_json, created_at
            FROM lookup_events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def add_favorite(barcode: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO favorites (barcode, created_at)
            VALUES (?, ?)
            ON CONFLICT(barcode) DO NOTHING
            """,
            (barcode, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def remove_favorite(barcode: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM favorites WHERE barcode = ?", (barcode,))
        connection.commit()
    return cursor.rowcount > 0


def list_favorites() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT barcode, created_at FROM favorites ORDER BY created_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def lookup_event_summary() -> dict[str, Any]:
    with get_connection() as connection:
        by_type_rows = connection.execute(
            """
            SELECT event_type, COUNT(*) as count
            FROM lookup_events
            GROUP BY event_type
            ORDER BY count DESC
            """
        ).fetchall()
        total_row = connection.execute("SELECT COUNT(*) AS total FROM lookup_events").fetchone()

    return {
        "total_events": total_row["total"] if total_row else 0,
        "by_type": {row["event_type"]: row["count"] for row in by_type_rows},
    }
