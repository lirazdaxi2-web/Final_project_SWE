"""The question, four answer buttons, a progress bar for the time, then the result."""
from tkinter import ttk


class QuestionView(ttk.Frame):

    def __init__(self, parent, on_answer):
        super().__init__(parent, padding=16)
        self.on_answer = on_answer
        # TODO stage 5: "Question 3 / 10" label, the question text (wraplength!),
        # four buttons in a 2x2 grid calling on_answer(0..3), a ttk.Progressbar
        # for the remaining time and a result label.
        raise NotImplementedError

    def show(self, payload: dict) -> None:
        """
        TODO stage 5: fill text + options, enable the buttons, reset the result
        label, and start a local countdown (after() every 100 ms) that only
        DISPLAYS time - the server is the authority on when time is up.
        """
        raise NotImplementedError

    def lock_buttons(self, chosen: int) -> None:
        """TODO stage 5: disable all four, highlight the chosen one."""
        raise NotImplementedError

    def show_result(self, payload: dict, my_name: str) -> None:
        """
        TODO stage 5: colour the correct option green, my wrong choice red,
        show "+800 points" (or "wrong / no answer") for me, and stop the countdown.
        """
        raise NotImplementedError
