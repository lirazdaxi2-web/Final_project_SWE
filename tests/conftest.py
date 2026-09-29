"""Shared pytest fixtures."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def temp_database(tmp_path, monkeypatch):
    """A Database on a throw-away file, schema created, singleton reset."""
    import config
    from langame.database.db import Database

    db_file = tmp_path / "test.db"
    monkeypatch.setattr(config, "DATABASE_PATH", str(db_file))
    Database._instance = None
    database = Database(str(db_file))
    database.initialize_schema()
    return database


@pytest.fixture
def sample_question():
    from langame.common.models import Question

    return Question(id=1, text="Which port does HTTP use?", options=["21", "25", "80", "443"],
                    correct_index=2, category="networks", difficulty=1)


class FakeHandler:
    """Stands in for ClientHandler: records what was sent, no socket."""

    def __init__(self, address="127.0.0.1:1"):
        self.address = address
        self.player_name = None
        self.sent = []

    def send(self, message):
        self.sent.append(message)
        return True


class FakeServer:
    """Stands in for GameServer: records broadcasts."""

    def __init__(self):
        self.broadcasts = []

    def broadcast(self, message, exclude_name=None):
        self.broadcasts.append(message)

    def remove_handler(self, handler):
        pass


@pytest.fixture
def fake_handler():
    return FakeHandler


@pytest.fixture
def fake_server():
    return FakeServer()
