"""
The client's connection to the server (the Model side of the client).

One background thread reads from the socket and pushes decoded messages
into a queue.Queue. The Tkinter thread drains the queue every 50 ms with
root.after() - Tkinter widgets must NEVER be touched from another thread.
"""
import queue
import socket
import threading
from typing import Optional

import config
from langame.common.protocol import Message, MessageBuffer, ProtocolError


class NetworkClient:

    def __init__(self):
        self._sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._buffer = MessageBuffer()
        self.inbox: "queue.Queue[Message]" = queue.Queue()
        self.connected = False

    def connect(self, host: str, port: int) -> None:
        """
        TODO stage 5: create the socket, connect((host, port)) with a timeout of
        a few seconds, then remove the timeout (settimeout(None)) for the
        reader, set connected=True and start _reader_loop in a daemon thread.
        Let socket errors propagate - the controller shows them to the user.
        """
        raise NotImplementedError

    def _reader_loop(self) -> None:
        """
        TODO stage 5: recv loop like ClientHandler.run(), but every decoded
        message goes to self.inbox.put(message). On disconnect put a special
        Message(MessageType.ERROR, {"code": "disconnected", ...}) so the UI
        can react, and set connected=False.
        """
        raise NotImplementedError

    def send(self, message: Message) -> None:
        """TODO stage 5: sendall(message.to_wire()); on OSError mark disconnected."""
        raise NotImplementedError

    def close(self) -> None:
        """TODO stage 5: idempotent; shutdown + close the socket."""
        raise NotImplementedError
