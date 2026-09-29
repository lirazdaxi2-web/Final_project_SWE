"""
Tests for the state machine. Target: end of stage 4.
No sockets: FakeHandler and FakeServer record what would have been sent.
"""
import pytest

import config
from langame.common.models import GameState
from langame.common.protocol import MessageType
from langame.server.commands import AnswerCommand, JoinCommand
from langame.server.game_engine import GameEngine


def make_engine(fake_server, monkeypatch):
    engine = GameEngine(server=fake_server, questions_per_game=2, time_limit=10.0, category=None)
    return engine


def test_join_adds_player_and_broadcasts_lobby(fake_server, fake_handler, monkeypatch):
    engine = make_engine(fake_server, monkeypatch)
    handler = fake_handler()
    engine.execute(JoinCommand(handler, "liraz"))
    assert "liraz" in engine.players
    assert handler.player_name == "liraz"
    assert engine.host_name == "liraz"
    assert handler.sent[0].type is MessageType.WELCOME
    assert fake_server.broadcasts[-1].type is MessageType.LOBBY_UPDATE


def test_duplicate_name_is_rejected(fake_server, fake_handler, monkeypatch):
    engine = make_engine(fake_server, monkeypatch)
    engine.execute(JoinCommand(fake_handler(), "liraz"))
    second = fake_handler("127.0.0.1:2")
    engine.execute(JoinCommand(second, "liraz"))
    assert second.player_name is None
    assert second.sent[-1].type is MessageType.ERROR
    assert second.sent[-1].payload["code"] == "name_taken"


def test_answer_in_lobby_is_rejected(fake_server, fake_handler, monkeypatch):
    engine = make_engine(fake_server, monkeypatch)
    handler = fake_handler()
    engine.execute(JoinCommand(handler, "liraz"))
    engine.execute(AnswerCommand(handler, question_id=1, choice=0))
    assert handler.sent[-1].type is MessageType.ERROR
    assert handler.sent[-1].payload["code"] == "not_accepting"


def test_second_answer_is_rejected(fake_server, fake_handler, monkeypatch, sample_question):
    engine = make_engine(fake_server, monkeypatch)
    handler = fake_handler()
    engine.execute(JoinCommand(handler, "liraz"))
    # put the engine straight into a question without timers or DB
    engine.state = GameState.QUESTION
    engine.current_question = sample_question
    engine.question_sent_at = 0.0
    engine.answers = {}
    monkeypatch.setattr(engine, "close_question", lambda: None)

    engine.execute(AnswerCommand(handler, question_id=1, choice=2))
    assert "liraz" in engine.answers
    engine.execute(AnswerCommand(handler, question_id=1, choice=0))
    assert handler.sent[-1].payload["code"] == "already_answered"
    assert engine.answers["liraz"].chosen_index == 2, "the first answer must stand"


def test_bad_choice_is_rejected(fake_server, fake_handler, monkeypatch, sample_question):
    engine = make_engine(fake_server, monkeypatch)
    handler = fake_handler()
    engine.execute(JoinCommand(handler, "liraz"))
    engine.state = GameState.QUESTION
    engine.current_question = sample_question
    engine.answers = {}
    monkeypatch.setattr(engine, "close_question", lambda: None)
    engine.execute(AnswerCommand(handler, question_id=1, choice=7))
    assert handler.sent[-1].payload["code"] == "bad_choice"


def test_public_payload_never_leaks_the_answer(sample_question):
    payload = sample_question.public_payload()
    assert "correct_index" not in payload
    assert payload["options"] == ["21", "25", "80", "443"]


def test_concurrent_answers_are_all_recorded(fake_server, fake_handler, monkeypatch, sample_question):
    """8 threads answer at the same instant - the lock must keep every record."""
    import threading

    engine = make_engine(fake_server, monkeypatch)
    handlers = [fake_handler(f"ip:{i}") for i in range(8)]
    for i, h in enumerate(handlers):
        engine.execute(JoinCommand(h, f"p{i}"))
    engine.state = GameState.QUESTION
    engine.current_question = sample_question
    engine.question_sent_at = 0.0
    engine.answers = {}
    monkeypatch.setattr(engine, "close_question", lambda: None)

    threads = [threading.Thread(target=engine.execute, args=(AnswerCommand(h, 1, 2),)) for h in handlers]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(engine.answers) == 8
