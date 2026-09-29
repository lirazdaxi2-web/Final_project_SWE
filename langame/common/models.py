"""
The entities the whole system talks about.

These are given to you complete except for the small methods marked TODO -
the field names here are the vocabulary of the protocol, the database and
the UI, so everything else depends on them staying exactly as they are.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class GameState(Enum):
    """The four states of the game's finite state machine (see GameEngine)."""

    LOBBY = "lobby"
    QUESTION = "question"
    SCORING = "scoring"
    GAME_OVER = "game_over"


@dataclass
class Question:
    id: int
    text: str
    options: List[str]           # exactly 4
    correct_index: int           # 0..3 - NEVER sent to the clients during a question
    category: str
    difficulty: int              # 1..3

    def public_payload(self) -> dict:
        """
        TODO stage 3: the dict that goes inside a QUESTION message:
        {"question_id", "text", "options"} - and nothing else. If correct_index
        leaks here, a modified client can cheat. Write a test for it.
        """
        raise NotImplementedError


@dataclass
class Player:
    name: str
    address: str                 # "ip:port" of the connection, for the log and the DB
    score: int = 0
    connected: bool = True
    joined_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None     # database id, set when the game is saved


@dataclass
class AnswerRecord:
    """One player's answer to one question, as measured by the SERVER."""

    player_name: str
    question_id: int
    chosen_index: int
    response_time: float         # seconds since the question was broadcast (server clock)
    is_correct: bool = False
    points: int = 0


@dataclass
class LeaderboardEntry:
    rank: int
    name: str
    score: int


def build_leaderboard(players: Dict[str, Player]) -> List[LeaderboardEntry]:
    """
    TODO stage 4: sort players by score (highest first), then by name for a
    stable order, and number them from 1. Disconnected players stay on the
    board - they still played.
    """
    raise NotImplementedError
