"""Tests for the persistence layer. Target: end of stage 3 (questions) and 6 (games)."""
from datetime import datetime

from langame.common.models import AnswerRecord, Player, Question
from langame.database.repositories import GameRepository, QuestionRepository


def make_question(text="Q?", category="general"):
    return Question(id=None, text=text, options=["a", "b", "c", "d"], correct_index=1,
                    category=category, difficulty=1)


def test_add_and_get(temp_database):
    repo = QuestionRepository(temp_database)
    qid = repo.add(make_question("Which port does HTTP use?", "networks"))
    loaded = repo.get(qid)
    assert loaded.id == qid
    assert loaded.options == ["a", "b", "c", "d"]
    assert loaded.correct_index == 1
    assert loaded.category == "networks"


def test_list_ids_filters_by_category(temp_database):
    repo = QuestionRepository(temp_database)
    repo.add(make_question("n1", "networks")); repo.add(make_question("n2", "networks")); repo.add(make_question("g1", "general"))
    assert len(repo.list_ids()) == 3
    assert len(repo.list_ids("networks")) == 2
    assert repo.count("general") == 1


def test_import_csv(temp_database, tmp_path):
    csv_file = tmp_path / "q.csv"
    csv_file.write_text(
        "text,option_a,option_b,option_c,option_d,correct_index,category,difficulty\n"
        "Q1,a,b,c,d,0,general,1\n"
        "Q2,a,b,c,d,3,networks,2\n"
        "BAD,a,b,c,d,9,general,1\n", encoding="utf-8")
    repo = QuestionRepository(temp_database)
    imported = repo.import_csv(str(csv_file))
    assert imported == 2
    assert repo.count() == 2


def test_save_game_writes_everything_in_one_transaction(temp_database):
    questions = QuestionRepository(temp_database)
    qid = questions.add(make_question())
    games = GameRepository(temp_database)
    players = {"a": Player("a", "ip:1", score=800), "b": Player("b", "ip:2", score=0)}
    answers = [AnswerRecord("a", qid, 1, 3.0, True, 800), AnswerRecord("b", qid, 0, 1.0, False, 0)]
    game_id = games.save_game(datetime(2026, 1, 1, 10, 0), datetime(2026, 1, 1, 10, 5), 1, 15.0, None, "a",
                              players, answers)
    recent = games.list_recent()
    assert recent[0]["id"] == game_id
    assert recent[0]["winner_name"] == "a"
    assert recent[0]["player_count"] == 2
