# Build plan — seven stages

For every stage: the files to touch, what to implement, and how to know it is done
("exit condition"). Do not move to the next stage before the exit condition is met.

Tick `[x]` when done — this file is also your progress log for the supervisor.

---

## Stage 1 — Protocol and infrastructure

- [ ] `langame/common/protocol.py` → `Message.to_wire`, `Message.from_wire`, `MessageBuffer.feed`
- [ ] A throw-away echo server + client (20 lines each, not part of the project) that exchange
      one JSON message over TCP on the same machine

**Exit condition:** `pytest tests/test_protocol.py -v` green. You can explain, with a drawing,
why the `\n` delimiter is needed (two messages glued / one message split).

---

## Stage 2 — Server and lobby

- [ ] `run_server.py` → `print_local_addresses`
- [ ] `langame/server/game_server.py` → `serve_forever`, `broadcast`, `remove_handler`, `shutdown`
- [ ] `langame/server/client_handler.py` → `run`, `_dispatch`, `send`, `close`
- [ ] `langame/server/commands.py` → `JoinCommand`, `LeaveCommand`, `build_command`
- [ ] `langame/server/game_engine.py` → `execute`, `add_player`, `player_left`, `lobby_payload`, `connected_players`

**Exit condition:** three terminal clients (a 10-line script that connects, sends JOIN and prints
what arrives) all receive the same LOBBY_UPDATE; closing one of them does not crash the server;
sending garbage returns an ERROR message. `pytest tests/test_game_engine.py -k "join or duplicate or lobby"` green.

---

## Stage 3 — Database and questions

- [ ] `langame/database/db.py` → `get_connection`, `connection`, `initialize_schema`
- [ ] `langame/database/repositories.py` → `QuestionRepository`: `add`, `get`, `list_ids`, `count`, `import_csv`
- [ ] `langame/common/models.py` → `Question.public_payload`
- [ ] `langame/server/question_manager.py` → `prepare`, `next`
- [ ] Import `data/questions_seed.csv` (a small script or the admin tool later)

**Exit condition:** `pytest tests/test_repositories.py -k "question or import" tests/test_game_engine.py::test_public_payload_never_leaks_the_answer -v` green.
`QuestionManager.prepare(10)` on the seed data gives 10 different ids; `prepare(100)` raises a clear error.

---

## Stage 4 — State machine and scoring

- [ ] `langame/server/score_engine.py` → `points_for`, `score_round`
- [ ] `langame/common/models.py` → `build_leaderboard`
- [ ] `langame/server/commands.py` → `StartGameCommand`, `AnswerCommand`
- [ ] `langame/server/game_engine.py` → `start_game`, `next_question`, `record_answer`, `close_question`,
      `result_payload`, `leaderboard_payload`

**Exit condition:** `pytest tests/test_score_engine.py tests/test_game_engine.py -v` all green —
including `test_concurrent_answers_are_all_recorded` (8 threads at once). A full game runs with
terminal clients: questions arrive, answers score, results and leaderboard are broadcast, the
game ends after N questions.

---

## Stage 5 — Graphical client

- [ ] `langame/client/network_client.py` → all four methods
- [ ] `langame/client/controllers/client_controller.py` → everything
- [ ] `langame/client/views/` → the five screens

**Exit condition:** two clients on one computer play a full game through the GUI: connect,
lobby with names, host presses Start, countdown, questions with a time bar, colours on the
result, live leaderboard, game-over screen. The window never freezes. Record a short video.

---

## Stage 6 — Admin tool and persistence

- [ ] `langame/database/repositories.py` → `QuestionRepository.update/delete/list_all/categories`,
      `GameRepository.save_game/list_recent`
- [ ] `langame/server/game_engine.py` → `end_game` (saves the game)
- [ ] `langame/admin/admin_app.py` → everything

**Exit condition:** `pytest -v` all green. A game played through the GUI appears in the admin's
"Games" tab with the right winner and players; a question added in the admin appears in the next game.

---

## Stage 7 — Load test, network analysis, documentation

- [ ] A game with 8 real players on the classroom network; note the time from broadcast to the
      last client's receipt (server log) — the "< 50 ms" metric
- [ ] Wireshark capture of one question round: TCP handshake, the JSON messages, ACKs — screenshots
      for the networks chapter
- [ ] `GameRepository.question_stats` (optional) — a table of hardest questions for the book
- [ ] Your own extra tests (at least: `build_command`, `QuestionManager.prepare`, `lobby_payload`)
- [ ] UML per `docs/UML.md`, the book per `docs/PROJECT_BOOK_MAP.md`
- [ ] Defense presentation + a demo video (in case the classroom network fails)

**Exit condition:** a complete project book where every number comes from a log, a test run or a capture.

---

## Success metrics from the proposal — tick at the end

| Metric | Target | Actual |
|---|---|---|
| Question reaches all players | < 50 ms | |
| Simultaneous players | 8 | |
| Concurrent-answer test | all 8 recorded, scores correct | |
| Player disconnect mid-question | game continues, server alive | |
| Malformed message | ERROR reply, state unchanged | |
| Question fetch | < 5 ms | |
| Unit-test coverage (protocol, scoring, engine) | ≥ 70% | |
| Full 10-question game with 4 players saved to DB | yes | |
