from __future__ import annotations

from contextlib import contextmanager
import sqlite3
from typing import Iterator


@contextmanager
def immediate_transaction(connection: sqlite3.Connection) -> Iterator[None]:
    """Run a write unit under SQLite's single-writer lock with safe rollback."""

    connection.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        connection.rollback()
        raise
    else:
        connection.commit()

