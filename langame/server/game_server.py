"""
Accepts TCP connections and gives each one a thread.

Threading model:
    main thread          accept() loop
    one thread / client  ClientHandler.run() - reads that client's messages
    one timer thread     closes a question when its time limit ends (in GameEngine)

Everything that touches shared game state goes through GameEngine, which
holds the single Lock. The server itself only accepts sockets and keeps the
list of handlers so it can broadcast and shut down cleanly.
"""
import logging
import socket
import threading
from typing import List, Optional

import config
from langame.server.game_engine import GameEngine

log = logging.getLogger("langame.server")


class GameServer:

    def __init__(self, port: int = config.SERVER_PORT, questions_per_game: int = config.QUESTIONS_PER_GAME,
                 time_limit: float = config.QUESTION_TIME_LIMIT, category: Optional[str] = None):
        self.port = port
        self.engine = GameEngine(server=self, questions_per_game=questions_per_game,
                                 time_limit=time_limit, category=category)
        self._listen_socket: Optional[socket.socket] = None
        self._handlers: List["ClientHandler"] = []     # noqa: F821 (imported in serve_forever)
        self._handlers_lock = threading.Lock()
        self._running = False

    def serve_forever(self) -> None:
        """
        TODO stage 2:
            1. create a TCP socket: socket.socket(AF_INET, SOCK_STREAM)
            2. setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  -> restart without "address in use"
            3. bind((config.SERVER_HOST, self.port)); listen(config.MAX_PLAYERS)
            4. settimeout(config.SOCKET_TIMEOUT_SECONDS) so accept() wakes up regularly
               and can notice self._running == False
            5. loop: try accept(); on socket.timeout continue; on a new connection
               create ClientHandler(conn, addr, self.engine), keep it in self._handlers
               (under the lock) and start its thread (daemon=True)
        Import ClientHandler inside the method to avoid a circular import.
        """
        raise NotImplementedError

    def broadcast(self, message, exclude_name: Optional[str] = None) -> None:
        """
        TODO stage 2: send `message` to every connected handler (skip exclude_name).
        Copy the handler list under the lock FIRST, then send outside the lock -
        a slow client must never block the others or hold the lock while writing.
        A handler whose send() fails is dropped through engine.player_left().
        """
        raise NotImplementedError

    def remove_handler(self, handler) -> None:
        """TODO stage 2: remove a finished handler from the list (under the lock)."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """
        TODO stage 2: set _running False, close every handler socket, close the
        listen socket, and ask the engine to save an in-progress game.
        """
        raise NotImplementedError
