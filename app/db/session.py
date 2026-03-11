from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eat_right_ai.db")


def _resolve_sqlite_path() -> str:
    if DATABASE_URL.startswith("sqlite:///"):
        raw_path = DATABASE_URL.replace("sqlite:///", "", 1)
        return str(Path(raw_path).resolve())
    return str(Path("eat_right_ai.db").resolve())


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(_resolve_sqlite_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()
