"""
The wire protocol: what a message looks like and how it is framed.

Every message is ONE JSON object on ONE line:

    {"type": "ANSWER", "payload": {"question_id": 17, "choice": 2}}\n

Why the newline: TCP is a stream of bytes with no message boundaries. Two
messages can arrive glued together, or one message can arrive in two pieces.
The "\n" at the end of every message is the frame boundary that lets the
receiver cut the stream back into messages. (JSON itself never contains a raw
newline, so the delimiter is safe.)

This module is used by BOTH the server and the client, so a change here is a
protocol change for everyone.
"""
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import config


class MessageType(str, Enum):
    # client -> server
    JOIN = "JOIN"                  # payload: {"name": str}
    ANSWER = "ANSWER"              # payload: {"question_id": int, "choice": int}
    LEAVE = "LEAVE"                # payload: {}
    START_GAME = "START_GAME"      # payload: {}   (only the first player / host may send)

    # server -> client
    WELCOME = "WELCOME"            # payload: {"name": str, "is_host": bool}
    LOBBY_UPDATE = "LOBBY_UPDATE"  # payload: {"players": [str], "min_players": int}
    COUNTDOWN = "COUNTDOWN"        # payload: {"seconds": int}
    QUESTION = "QUESTION"          # payload: {"question_id", "text", "options", "time_limit", "number", "total"}
    RESULT = "RESULT"              # payload: {"question_id", "correct_index", "answers": [{name, choice, is_correct, points}]}
    LEADERBOARD = "LEADERBOARD"    # payload: {"entries": [{"rank", "name", "score"}]}
    GAME_OVER = "GAME_OVER"        # payload: {"winner": str, "entries": [...]}
    ERROR = "ERROR"                # payload: {"code": str, "message": str}


@dataclass
class Message:
    type: MessageType
    payload: Dict[str, Any]

    def to_wire(self) -> bytes:
        """
        TODO stage 1: serialise to bytes ready for socket.sendall():
            json.dumps({"type": self.type.value, "payload": self.payload})
            + config.MESSAGE_DELIMITER, encoded with config.ENCODING.
        Use ensure_ascii=False so Hebrew question text stays readable in logs.
        """
        raise NotImplementedError

    @classmethod
    def from_wire(cls, line: str) -> "Message":
        """
        TODO stage 1: parse ONE line (without the trailing newline).
        Raise ProtocolError (below) - never a raw json/KeyError - when:
            * the JSON is invalid
            * "type" is missing or not a known MessageType
            * "payload" is missing or not a dict
        The server must survive garbage from a broken or malicious client.
        """
        raise NotImplementedError


class ProtocolError(ValueError):
    """Raised for any malformed message. Carries a short machine-readable code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class MessageBuffer:
    """
    Turns the byte stream from a socket back into whole messages.

    Usage on the receiving side:
        buffer = MessageBuffer()
        chunk = sock.recv(4096)
        for message in buffer.feed(chunk):
            handle(message)

    Keep whatever is left after the last "\n" - it is the beginning of the
    next message and will be completed by the next recv().
    """

    def __init__(self):
        self._pending = b""

    def feed(self, chunk: bytes) -> List[Message]:
        """
        TODO stage 1:
            1. self._pending += chunk
            2. if len(self._pending) > config.MAX_MESSAGE_BYTES: raise ProtocolError("too_large", ...)
            3. split on the delimiter; the LAST piece is incomplete -> keep it in _pending
            4. decode every complete line and return the list of Message objects
               (an empty line is ignored)
        """
        raise NotImplementedError


# ── Convenience constructors (complete) ────────────────────────────

def error(code: str, message: str) -> Message:
    return Message(MessageType.ERROR, {"code": code, "message": message})


def join(name: str) -> Message:
    return Message(MessageType.JOIN, {"name": name})


def answer(question_id: int, choice: int) -> Message:
    return Message(MessageType.ANSWER, {"question_id": question_id, "choice": choice})
