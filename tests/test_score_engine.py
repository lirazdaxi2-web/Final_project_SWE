"""Tests for ScoreEngine and the leaderboard. Target: end of stage 4."""
import pytest

import config
from langame.common.models import AnswerRecord, Player, build_leaderboard
from langame.server.score_engine import ScoreEngine


def test_fast_correct_answer_scores_high():
    engine = ScoreEngine(time_limit=15.0)
    assert engine.points_for(True, 3.0) == 800


def test_instant_answer_scores_max():
    assert ScoreEngine(15.0).points_for(True, 0.0) == config.MAX_POINTS


def test_slow_correct_answer_never_below_minimum():
    assert ScoreEngine(15.0).points_for(True, 14.9) == config.MIN_POINTS_CORRECT


def test_wrong_answer_scores_zero():
    assert ScoreEngine(15.0).points_for(False, 0.5) == 0


def test_response_time_is_clamped():
    engine = ScoreEngine(15.0)
    assert engine.points_for(True, 99.0) == config.MIN_POINTS_CORRECT
    assert engine.points_for(True, -1.0) == config.MAX_POINTS


def test_score_round_updates_players(sample_question):
    engine = ScoreEngine(15.0)
    players = {"a": Player("a", "ip:1"), "b": Player("b", "ip:2"), "c": Player("c", "ip:3")}
    answers = {
        "a": AnswerRecord("a", 1, chosen_index=2, response_time=3.0),    # correct, 800
        "b": AnswerRecord("b", 1, chosen_index=0, response_time=1.0),    # wrong
    }
    engine.score_round(sample_question, answers, players)
    assert answers["a"].is_correct and answers["a"].points == 800
    assert not answers["b"].is_correct and answers["b"].points == 0
    assert players["a"].score == 800
    assert players["b"].score == 0
    assert players["c"].score == 0          # did not answer


def test_leaderboard_is_sorted_and_ranked():
    players = {"a": Player("a", "ip", score=300), "b": Player("b", "ip", score=900), "c": Player("c", "ip", score=300)}
    board = build_leaderboard(players)
    assert [(e.rank, e.name) for e in board] == [(1, "b"), (2, "a"), (3, "c")]
