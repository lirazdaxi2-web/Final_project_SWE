"""
The window: a stack of screens, one visible at a time.

    ConnectView  ->  LobbyView  ->  QuestionView (+ LeaderboardView on the side)  ->  GameOverView

Use one container Frame and tkraise() the active screen - simpler than
destroying and recreating widgets. The views never import the protocol;
they receive plain dicts/lists from the controller.
"""
import tkinter as tk
from tkinter import ttk


class MainWindow(ttk.Frame):

    def __init__(self, root: tk.Tk, on_connect, on_answer, on_start, default_host: str, default_port: int):
        super().__init__(root, padding=8)
        self.pack(fill="both", expand=True)
        # TODO stage 5: create ConnectView, LobbyView, QuestionView, LeaderboardView,
        # GameOverView in a shared container with grid(row=0, column=0, sticky="nsew"),
        # keep them as attributes (self.connect, self.lobby, self.question, ...),
        # and pass the callbacks through.
        raise NotImplementedError

    def show(self, name: str) -> None:
        """TODO stage 5: tkraise() the screen called `name`."""
        raise NotImplementedError

    def show_error(self, text: str) -> None:
        """TODO stage 5: messagebox.showerror - the only place tkinter.messagebox is imported."""
        raise NotImplementedError
