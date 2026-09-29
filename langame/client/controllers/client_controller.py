"""
The client's controller: messages in -> screen updates; button clicks -> messages out.

    server ──▶ NetworkClient.inbox ──(root.after 50ms)──▶ handle_message() ──▶ views
    views  ──▶ on_join / on_answer / on_start ──▶ NetworkClient.send()

This is the only class in the client that knows both the protocol and the views.
"""
import queue
import tkinter as tk

import config
from langame.common.protocol import Message, MessageType, answer, join
from langame.client.network_client import NetworkClient

POLL_MS = 50


class ClientController:

    def __init__(self, root: tk.Tk, default_host: str, default_port: int):
        self.root = root
        self.net = NetworkClient()
        self.player_name = ""
        self.is_host = False
        self.current_question_id = None
        self.has_answered = False

        # TODO stage 5: build the MainWindow and give it the callbacks:
        #   self.view = MainWindow(root, on_connect=self.on_connect, on_answer=self.on_answer,
        #                          on_start=self.on_start, default_host=..., default_port=...)
        #   root.protocol("WM_DELETE_WINDOW", self.on_close)
        raise NotImplementedError

    def start(self) -> None:
        """TODO stage 5: show the connect screen and schedule _poll_inbox."""
        raise NotImplementedError

    # ── from the views ──────────────────────────────────────────────

    def on_connect(self, host: str, port: int, name: str) -> None:
        """
        TODO stage 5: validate the name locally (non-empty, length), then
        net.connect(host, port) inside try/except -> view.show_error on failure;
        on success send join(name) and show the lobby screen (waiting state).
        """
        raise NotImplementedError

    def on_start(self) -> None:
        """TODO stage 5: host only - send START_GAME."""
        raise NotImplementedError

    def on_answer(self, choice: int) -> None:
        """
        TODO stage 5: ignore if has_answered; send answer(current_question_id, choice);
        has_answered = True; view.question.lock_buttons(choice).
        """
        raise NotImplementedError

    def on_close(self) -> None:
        """TODO stage 5: send LEAVE (best effort), net.close(), root.destroy()."""
        raise NotImplementedError

    # ── from the server ─────────────────────────────────────────────

    def _poll_inbox(self) -> None:
        """
        TODO stage 5: drain net.inbox with get_nowait() in a loop (catch queue.Empty),
        call handle_message on each, then root.after(POLL_MS, self._poll_inbox).
        """
        raise NotImplementedError

    def handle_message(self, message: Message) -> None:
        """
        TODO stage 5: one branch per MessageType (a dict of handlers is cleaner than if/elif):
            WELCOME       -> remember name/is_host; lobby.set_host_controls(is_host)
            LOBBY_UPDATE  -> lobby.set_players(names, min_players)
            COUNTDOWN     -> lobby.show_countdown(seconds)
            QUESTION      -> remember id; has_answered=False; question.show(payload); start the local countdown
            RESULT        -> question.show_result(payload, my_name)
            LEADERBOARD   -> leaderboard.update(entries)
            GAME_OVER     -> show the game-over screen with winner + entries
            ERROR         -> view.show_error(message); "disconnected" also returns to the connect screen
        """
        raise NotImplementedError
