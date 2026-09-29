"""
Command pattern: every client action is an object with execute(engine).

Why: the handler thread only *builds* the command; the engine *executes* it
under its lock. Rules live in one place, new actions are one new class, and
the list of executed commands is a complete replay of the game (nice for the
project book and for debugging).
"""
from abc import ABC, abstractmethod
from typing import Optional

from langame.common.protocol import Message, MessageType, ProtocolError


class Command(ABC):

    def __init__(self, handler):
        self.handler = handler          # the ClientHandler that received the message

    @abstractmethod
    def execute(self, engine) -> Optional[Message]:
        """
        Apply the command to the engine. Called WITH the engine lock held.
        Return an ERROR message to send back to this client, or None.
        """


class JoinCommand(Command):

    def __init__(self, handler, name: str):
        super().__init__(handler)
        self.name = name

    def execute(self, engine) -> Optional[Message]:
        """
        TODO stage 2: validate (state must be LOBBY, name non-empty and unique,
        <= PLAYER_NAME_MAX_LENGTH, room for one more player); on success
        engine.add_player(self.name, self.handler) and return None; otherwise
        return an ERROR with codes like "game_started", "name_taken", "full".
        """
        raise NotImplementedError


class StartGameCommand(Command):

    def execute(self, engine) -> Optional[Message]:
        """TODO stage 4: only the host may start, and only with >= MIN_PLAYERS."""
        raise NotImplementedError


class AnswerCommand(Command):

    def __init__(self, handler, question_id: int, choice: int):
        super().__init__(handler)
        self.question_id = question_id
        self.choice = choice

    def execute(self, engine) -> Optional[Message]:
        """
        TODO stage 4: engine.record_answer(self.handler.player_name,
        self.question_id, self.choice). The engine itself checks state,
        question id, 0 <= choice <= 3 and "already answered".
        """
        raise NotImplementedError


class LeaveCommand(Command):

    def execute(self, engine) -> Optional[Message]:
        """TODO stage 2: engine.player_left(self.handler.player_name)."""
        raise NotImplementedError


def build_command(message: Message, handler) -> Command:
    """
    Factory: message -> Command object.

    TODO stage 2: map MessageType.JOIN / ANSWER / LEAVE / START_GAME to the
    classes above, pulling fields out of message.payload. Missing or wrongly
    typed fields raise ProtocolError("bad_payload", ...). Any other type
    raises ProtocolError("unexpected_type", ...).
    """
    raise NotImplementedError
