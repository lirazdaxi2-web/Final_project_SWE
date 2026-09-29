"""Turns answers into points."""
from typing import Dict

import config
from langame.common.models import AnswerRecord, Player, Question


class ScoreEngine:
    """
    Points for a correct answer fall linearly with response time:

        points = round(MAX_POINTS * (time_limit - response_time) / time_limit)
        never below MIN_POINTS_CORRECT for a correct answer; 0 for a wrong one.

    Example with time_limit = 15:
        answered in 3.0 s  -> 1000 * 12 / 15 = 800
        answered in 14.9 s -> 1000 * 0.1 / 15 = 7  -> raised to 100
        wrong              -> 0

    The engine calls score_round() with the lock held, so this class does not
    need its own lock - but it must never be called from anywhere else.
    """

    def __init__(self, time_limit: float):
        self.time_limit = time_limit

    def points_for(self, is_correct: bool, response_time: float) -> int:
        """TODO stage 4: the formula above. Clamp response_time to [0, time_limit]."""
        raise NotImplementedError

    def score_round(self, question: Question, answers: Dict[str, AnswerRecord],
                    players: Dict[str, Player]) -> None:
        """
        TODO stage 4: for every answer: set is_correct and points, and add the
        points to players[name].score. Players who did not answer get 0 and
        no AnswerRecord (the result payload shows them as "no answer").
        """
        raise NotImplementedError
