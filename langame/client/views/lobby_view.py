"""Who is here, how many are needed, and the host's Start button."""
from tkinter import ttk


class LobbyView(ttk.Frame):

    def __init__(self, parent, on_start):
        super().__init__(parent, padding=20)
        self.on_start = on_start
        # TODO stage 5: a Listbox of player names, a status label
        # ("3 / 2 players - waiting for host"), a Start button (hidden unless host),
        # and a big countdown label.
        raise NotImplementedError

    def set_players(self, names, min_players: int) -> None:
        """TODO stage 5: refresh the list and the status label."""
        raise NotImplementedError

    def set_host_controls(self, is_host: bool) -> None:
        """TODO stage 5: show/enable the Start button only for the host."""
        raise NotImplementedError

    def show_countdown(self, seconds: int) -> None:
        """TODO stage 5: "Game starts in 5..." counting down locally with after()."""
        raise NotImplementedError
