"""
Question management (CRUD) + CSV import + game history.

Talks ONLY to QuestionRepository / GameRepository. If you find yourself
writing SQL here, stop and add a repository method instead.
"""
import tkinter as tk
from tkinter import ttk

from langame.database.repositories import GameRepository, QuestionRepository


class AdminApp(ttk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root, padding=8)
        self.questions = QuestionRepository()
        self.games = GameRepository()
        # TODO stage 6: a ttk.Notebook with two tabs:
        #   "Questions": Treeview (id, text, category, difficulty) + a form
        #                (text, 4 options, correct radio, category, difficulty)
        #                + buttons Add / Update / Delete / Import CSV / Refresh
        #   "Games":     Treeview of GameRepository.list_recent()
        raise NotImplementedError

    def refresh_questions(self) -> None:
        """TODO stage 6: reload the table from questions.list_all()."""
        raise NotImplementedError

    def on_add(self) -> None:
        """TODO stage 6: read the form, validate (4 non-empty options, a correct one), questions.add()."""
        raise NotImplementedError

    def on_update(self) -> None:
        """TODO stage 6: questions.update() for the selected row."""
        raise NotImplementedError

    def on_delete(self) -> None:
        """TODO stage 6: confirm with messagebox.askyesno, then questions.delete()."""
        raise NotImplementedError

    def on_import_csv(self) -> None:
        """TODO stage 6: filedialog.askopenfilename -> questions.import_csv(path) -> show the count."""
        raise NotImplementedError

    def refresh_games(self) -> None:
        """TODO stage 6: reload from games.list_recent()."""
        raise NotImplementedError
