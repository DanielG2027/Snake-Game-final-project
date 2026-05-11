from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from snake import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  score INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_scores_score ON scores(score);
"""


@dataclass(frozen=True)
class ScoreRow:
    score: int
    created_at: str


class ScoresRepo:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or config.runtime_path(config.SCORES_DB_NAME)

    def init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def add_score(self, score: int) -> None:
        if score < 0:
            raise ValueError("score must be >= 0")
        self.init_db()
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.execute("INSERT INTO scores (score) VALUES (?)", (score,))
            conn.commit()

    def top_n(self, n: int = 10) -> list[ScoreRow]:
        self.init_db()
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT score, created_at FROM scores ORDER BY score DESC, id DESC LIMIT ?",
                (n,),
            ).fetchall()
        return [
            ScoreRow(score=int(score), created_at=str(created_at)) for score, created_at in rows
        ]

    def best_score(self) -> int:
        self.init_db()
        with closing(sqlite3.connect(self.db_path)) as conn:
            row = conn.execute("SELECT MAX(score) FROM scores").fetchone()
        value = row[0] if row else None
        return int(value) if value is not None else 0

    def qualifies(self, score: int, *, n: int = 10) -> bool:
        if score < 0:
            raise ValueError("score must be >= 0")
        self.init_db()
        rows = self.top_n(n)
        if len(rows) < n:
            return True
        return score >= rows[-1].score
