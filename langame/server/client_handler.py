"""
One thread per connected client.

Reads bytes from the socket, cuts them into messages with MessageBuffer,
turns each message into a Command and hands it to the engine. This class
knows nothing about game rules - that is the engine's job - and the engine
knows nothing about sockets - that is this class's job.
"""
import logging
import socket
import threading
from typing import Optional

import config
from langame.common.protocol import Message, MessageBuffer, ProtocolError, error
from langame.server.commands import build_command

log = logging.getLogger("langame.handler")


class ClientHandler(threading.Thread):

    def __init__(self, conn: socket.socket, address: tuple, engine):
        super().__init__(daemon=True, name=f"client-{address[0]}:{address[1]}")
        self.conn = conn
        self.address = f"{address[0]}:{address[1]}"
        self.engine = engine
        self.player_name: Optional[str] = None      # set by JoinCommand once accepted
        self._buffer = MessageBuffer()
        self._send_lock = threading.Lock()          # two threads may send to the same client
        self._alive = True

    def run(self) -> None:
        """
        TODO stage 2:
            conn.settimeout(config.SOCKET_TIMEOUT_SECONDS)
            while self._alive:
                try: chunk = conn.recv(config.RECV_BUFFER_SIZE)
                except socket.timeout: continue
                except OSError: break
                if not chunk: break                       # client closed the connection
                try:
                    for message in self._buffer.feed(chunk):
                        self._dispatch(message)
                except ProtocolError as exc:
                    self.send(error(exc.code, str(exc)))  # tell the client, keep serving
            finally: self.close()
        """
        raise NotImplementedError

    def _dispatch(self, message: Message) -> None:
        """
        TODO stage 2: command = build_command(message, self); self.engine.execute(command).
        Unknown/illegal commands come back from the engine as an ERROR message
        to send - the handler never decides rules by itself.
        """
        raise NotImplementedError

    def send(self, message: Message) -> bool:
        """
        TODO stage 2: conn.sendall(message.to_wire()) under _send_lock.
        Return False (and mark not alive) on any OSError instead of raising -
        the caller may be the broadcaster iterating over all clients.
        """
        raise NotImplementedError

    def close(self) -> None:
        """
        TODO stage 2: idempotent. Mark not alive, tell the engine the player left
        (only if player_name is set), close the socket, remove self from the server.
        """
        raise NotImplementedError
