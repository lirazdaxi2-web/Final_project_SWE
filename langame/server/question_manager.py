"""Picks questions for one game with no repeats."""
import random
from typing import List, Optional

from langame.common.models import Question


class QuestionManager:
    """
    Efficient random selection: load the matching ids ONCE, shuffle them in
    Python, then fetch each question by id. `ORDER BY RANDOM()` on the whole
    table would rescan it for every question and could repeat questions.
    """

    def __init__(self, repository, category: Optional[str] = None):
        self.repository = repository
        self.category = category
        self._queue: List[int] = []

    def prepare(self, count: int) -> None:
        """
        TODO stage 3: ids = repository.list_ids(category); shuffle; keep the
        first `count`. Raise ValueError with a clear message if there are fewer
        than `count` questions - better than crashing mid-game.
        """
        raise NotImplementedError

    def next(self) -> Question:
        """TODO stage 3: pop the next id and return repository.get(id)."""
        raise NotImplementedError

    @property
    def remaining(self) -> int:
        return len(self._queue)
