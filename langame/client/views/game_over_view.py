"""Winner + final table + 'back to lobby'."""
from tkinter import ttk


class GameOverView(ttk.Frame):

    def __init__(self, parent, on_back):
        super().__init__(parent, padding=20)
        self.on_back = on_back
        # TODO stage 5: winner label, a Treeview of final scores, a Back button.
        raise NotImplementedError

    def show(self, winner: str, entries) -> None:
        """TODO stage 5."""
        raise NotImplementedError
