"""
SQLite connection management.

The schema is given complete - it is the database chapter of the project
book. Only the Python methods are left to implement.
"""
import sqlite3
from contextlib import contextmanager

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    text          TEXT    NOT NULL,
    option_a      TEXT    NOT NULL,
    option_b      TEXT    NOT NULL,
    option_c      TEXT    NOT NULL,
    option_d      TEXT    NOT NULL,
    correct_index INTEGER NOT NULL CHECK (correct_index BETWEEN 0 AND 3),
    category      TEXT    NOT NULL DEFAULT 'general',
    difficulty    INTEGER NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 3),
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_questions_cat_diff ON questions (category, difficulty);

CREATE TABLE IF NOT EXISTS games (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at          TEXT    NOT NULL,
    ended_at            TEXT,
    questions_count     INTEGER NOT NULL,
    time_limit          REAL    NOT NULL,
    category            TEXT,
    winner_name         TEXT
);

CREATE TABLE IF NOT EXISTS players (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id     INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    address     TEXT    NOT NULL,
    joined_at   TEXT    NOT NULL,
    final_score INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_players_game ON players (game_id);

CREATE TABLE IF NOT EXISTS answers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id       INTEGER NOT NULL,
    player_id     INTEGER NOT NULL,
    question_id   INTEGER NOT NULL,
    chosen_index  INTEGER NOT NULL,
    is_correct    INTEGER NOT NULL,          -- 0 / 1 (SQLite has no BOOLEAN)
    response_time REAL    NOT NULL,
    points        INTEGER NOT NULL,
    FOREIGN KEY (game_id)     REFERENCES games (id)     ON DELETE CASCADE,
    FOREIGN KEY (player_id)   REFERENCES players (id)   ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions (id)
);
CREATE INDEX IF NOT EXISTS idx_answers_question ON answers (question_id);
"""


class Database:
    """Singleton owning the connection factory (see docs/UML.md)."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """
        TODO stage 3:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")     # off by default in SQLite!
            return conn
        check_same_thread=False: the server writes from the engine's thread,
        the timer thread and the handler threads. Each call still opens its
        own short-lived connection, so there is no sharing across threads.
        """
        raise NotImplementedError

    @contextmanager
    def connection(self):
        """
        TODO stage 3: commit on success, rollback on any exception, always close.
        """
        raise NotImplementedError

    def initialize_schema(self) -> None:
        """TODO stage 3: conn.executescript(SCHEMA)."""
        raise NotImplementedError
