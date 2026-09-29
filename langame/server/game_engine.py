"""
The heart of the server: a finite state machine that owns ALL game state.

    LOBBY ──start──▶ QUESTION ──time up / all answered──▶ SCORING
      ▲                 ▲                                    │
      │                 └──────── next question ─────────────┤
      │                                                      │ last question
      └──────────── new game ◀──── GAME_OVER ◀───────────────┘

Rules of this class:
    * every public method takes self._lock first - the handlers call them
      from many threads at once
    * it never touches sockets directly; it talks to the world through
      self.server.broadcast() and handler.send()
    * it never touches SQL directly; it uses the repositories
"""
import logging
import threading
import time
from typing import Dict, List, Optional

import config
from langame.common.models import AnswerRecord, GameState, Player, Question, build_leaderboard
from langame.common.protocol import Message, MessageType, error
from langame.database.repositories import GameRepository, QuestionRepository
from langame.server.question_manager import QuestionManager
from langame.server.score_engine import ScoreEngine

log = logging.getLogger("langame.engine")


class GameEngine:

    def __init__(self, server, questions_per_game: int, time_limit: float, category: Optional[str]):
        self.server = server
        self.questions_per_game = questions_per_game
        self.time_limit = time_limit
        self.category = category

        self._lock = threading.RLock()          # RLock: execute() may call methods that lock again
        self.state = GameState.LOBBY
        self.players: Dict[str, Player] = {}    # name -> Player
        self.handlers: Dict[str, object] = {}   # name -> ClientHandler
        self.host_name: Optional[str] = None    # first player to join

        self.questions = QuestionManager(QuestionRepository(), category)
        self.scores = ScoreEngine(time_limit)
        self.current_question: Optional[Question] = None
        self.question_number = 0
        self.question_sent_at: float = 0.0      # time.monotonic() when broadcast
        self.answers: Dict[str, AnswerRecord] = {}   # name -> answer for the current question
        self._question_timer: Optional[threading.Timer] = None
        self.started_at: Optional[float] = None
        self.history: List[AnswerRecord] = []   # every answer of the game, for the DB

    # ── entry point used by ClientHandler ──────────────────────────

    def execute(self, command) -> None:
        """
        TODO stage 2: with self._lock: reply = command.execute(self);
        if reply is not None: command.handler.send(reply).
        Log every command with its player name and the current state.
        """
        raise NotImplementedError

    # ── lobby ───────────────────────────────────────────────────────

    def add_player(self, name: str, handler) -> None:
        """
        TODO stage 2: create Player(name, handler.address), store player and
        handler, set handler.player_name, make the first player the host,
        send WELCOME to that handler and broadcast a LOBBY_UPDATE.
        """
        raise NotImplementedError

    def player_left(self, name: Optional[str]) -> None:
        """
        TODO stage 2: mark the player disconnected and drop its handler.
        In LOBBY: remove the player entirely and re-pick the host if needed.
        In QUESTION: if everyone still connected has answered, close the question.
        Always broadcast LOBBY_UPDATE (lobby) or nothing (in-game) - never crash.
        """
        raise NotImplementedError

    def lobby_payload(self) -> dict:
        """TODO stage 2: {"players": [names of connected players], "min_players": ...}."""
        raise NotImplementedError

    # ── game flow ───────────────────────────────────────────────────

    def start_game(self) -> None:
        """
        TODO stage 4: state -> QUESTION path: load the question pool
        (self.questions.prepare(self.questions_per_game)), reset scores,
        record started_at, broadcast COUNTDOWN and schedule next_question()
        with a threading.Timer of LOBBY_COUNTDOWN_SECONDS.
        """
        raise NotImplementedError

    def next_question(self) -> None:
        """
        TODO stage 4:
            if question_number == questions_per_game: return self.end_game()
            question = self.questions.next(); question_number += 1
            answers = {}; state = QUESTION; question_sent_at = time.monotonic()
            broadcast QUESTION with question.public_payload() + time_limit/number/total
            start self._question_timer = Timer(time_limit, self.close_question)
        """
        raise NotImplementedError

    def record_answer(self, name: str, question_id: int, choice: int) -> Optional[Message]:
        """
        TODO stage 4: the most important validation in the project.
            reject (return ERROR) when: state != QUESTION ("not_accepting"),
            question_id != current ("stale_question"), choice not in 0..3
            ("bad_choice"), name already in self.answers ("already_answered").
            otherwise store AnswerRecord(name, question_id, choice,
            response_time=time.monotonic() - question_sent_at) and return None.
            If every connected player has now answered -> close_question() early.
        """
        raise NotImplementedError

    def close_question(self) -> None:
        """
        TODO stage 4: called by the timer OR by record_answer. Must be safe to
        call twice (cancel the timer; ignore if state != QUESTION).
            state = SCORING
            self.scores.score_round(self.current_question, self.answers, self.players)
            history.extend(answers.values())
            broadcast RESULT then LEADERBOARD
            Timer(SECONDS_BETWEEN_QUESTIONS, self.next_question).start()
        """
        raise NotImplementedError

    def end_game(self) -> None:
        """
        TODO stage 6: state = GAME_OVER; build the leaderboard; broadcast
        GAME_OVER with the winner; save everything with GameRepository.save_game(...);
        then reset to a fresh LOBBY so players can play again.
        """
        raise NotImplementedError

    # ── helpers ─────────────────────────────────────────────────────

    def result_payload(self) -> dict:
        """TODO stage 4: correct_index + one entry per player (choice, is_correct, points)."""
        raise NotImplementedError

    def leaderboard_payload(self) -> dict:
        """TODO stage 4: {"entries": [asdict(e) for e in build_leaderboard(self.players)]}."""
        raise NotImplementedError

    def connected_players(self) -> List[Player]:
        """TODO stage 2: players with connected == True."""
        raise NotImplementedError
