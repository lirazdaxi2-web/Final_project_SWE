"""
Repository pattern - one class per aggregate. No SQL anywhere else.
"""
import csv
from datetime import datetime
from typing import Dict, List, Optional

from langame.common.models import AnswerRecord, Player, Question
from langame.database.db import Database


class QuestionRepository:

    def __init__(self, database: Database = None):
        self.db = database or Database()

    def add(self, question: Question) -> int:
        """TODO stage 3: INSERT and return the new id. created_at = now().isoformat()."""
        raise NotImplementedError

    def update(self, question: Question) -> None:
        """TODO stage 6: UPDATE every editable column WHERE id=?."""
        raise NotImplementedError

    def delete(self, question_id: int) -> None:
        """TODO stage 6: DELETE WHERE id=?."""
        raise NotImplementedError

    def get(self, question_id: int) -> Optional[Question]:
        """TODO stage 3: SELECT one row and map it to a Question (options as a list of 4)."""
        raise NotImplementedError

    def list_ids(self, category: Optional[str] = None) -> List[int]:
        """
        TODO stage 3: SELECT id ... optionally WHERE category=?.
        Only ids - this is what QuestionManager shuffles.
        """
        raise NotImplementedError

    def list_all(self, category: Optional[str] = None) -> List[Question]:
        """TODO stage 6: for the admin table."""
        raise NotImplementedError

    def categories(self) -> List[str]:
        """TODO stage 6: SELECT DISTINCT category ORDER BY category."""
        raise NotImplementedError

    def count(self, category: Optional[str] = None) -> int:
        """TODO stage 3: SELECT COUNT(*) ..."""
        raise NotImplementedError

    def import_csv(self, path: str) -> int:
        """
        TODO stage 3: read data/questions_seed.csv (columns: text, option_a,
        option_b, option_c, option_d, correct_index, category, difficulty) and
        insert every row in ONE transaction with executemany. Return how many
        were imported. Skip rows with a bad correct_index and report them.
        """
        raise NotImplementedError


class GameRepository:

    def __init__(self, database: Database = None):
        self.db = database or Database()

    def save_game(self, started_at: datetime, ended_at: datetime, questions_count: int,
                  time_limit: float, category: Optional[str], winner_name: Optional[str],
                  players: Dict[str, Player], answers: List[AnswerRecord]) -> int:
        """
        TODO stage 6: ONE transaction that inserts the game, then every player
        (remember the new player ids in a dict name -> id), then every answer
        with the right player_id. Return the game id. If anything fails
        nothing is written - that is what the transaction is for.
        """
        raise NotImplementedError

    def list_recent(self, limit: int = 20) -> List[dict]:
        """TODO stage 6: newest games first with winner and player count (a JOIN + GROUP BY)."""
        raise NotImplementedError

    def question_stats(self) -> List[dict]:
        """
        TODO stage 7 (optional): per question: how many times asked, % correct,
        average response time. A great table for the project book:
            SELECT q.id, q.text, COUNT(a.id) AS asked,
                   AVG(a.is_correct) AS pct_correct, AVG(a.response_time) AS avg_time
            FROM questions q LEFT JOIN answers a ON a.question_id = q.id
            GROUP BY q.id ORDER BY pct_correct
        """
        raise NotImplementedError
