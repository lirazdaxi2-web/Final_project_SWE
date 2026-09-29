"""Live ranking, shown next to the question."""
from tkinter import ttk


class LeaderboardView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        # TODO stage 5: a ttk.Treeview with columns rank / name / score.
        raise NotImplementedError

    def update(self, entries) -> None:
        """TODO stage 5: clear and refill from [{"rank", "name", "score"}, ...]."""
        raise NotImplementedError

    def highlight(self, my_name: str) -> None:
        """TODO stage 5 (optional): bold / coloured row for the local player."""
        raise NotImplementedError
