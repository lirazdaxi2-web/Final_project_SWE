# LanGame — Final Project No. 5

**Multiplayer LAN trivia game** (client / server)
Atid – Western Galilee | Software Engineering, Grade 14 | 2025–2026
Student: Liraz Dakseh

---

## What this folder is

This is a **skeleton** of the project: the folder structure, every class, every function
signature, the documentation and the explanations — but **without the implementation**.
Every function is marked `TODO` and raises `NotImplementedError`, and next to it are the
exact steps to implement.

The code you write is your project. The skeleton exists so you do not waste time on
architecture decisions and on "where does what go", and so the structure meets the Ministry's
requirements from the start: OOP, design patterns, a database, separation of layers, tests.

**Do not delete the documentation in the files.** It was written so you understand what you
are building, and it is also the base for the chapters of the project book.

---

## Installation

Everything the game needs is in Python's standard library. Only the test runner is extra.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

Check that Tkinter is present (it comes with the official Python installer on Windows):

```bash
python -c "import tkinter; print('tk ok')"
```

---

## Running

```bash
python run_server.py                 # 1. the server (one machine in the room)
python run_client.py --host <ip>     # 2. one per player (the server prints its IP)
python run_admin.py                  # 3. the teacher's tool: questions + history
pytest -v                            # unit tests
```

In the first stages every command fails with `NotImplementedError` — that is normal, it fails
exactly at the place you have not implemented yet.

To test alone on one computer: run the server, then two or three clients with `--host 127.0.0.1`.

---

## Project structure

```
LanGame/
├── config.py                  all settings — complete, no need to change at first
├── run_server.py              starts the server
├── run_client.py              starts a player client
├── run_admin.py               starts the admin tool
│
├── langame/
│   ├── common/                shared by all three programs
│   │   ├── protocol.py        the messages (JSON over TCP) and the framing
│   │   └── models.py          Question, Player, AnswerRecord, GameState, leaderboard
│   ├── server/
│   │   ├── game_server.py     accepts connections, one thread per client, broadcast
│   │   ├── client_handler.py  reads one client's messages -> Commands
│   │   ├── commands.py        Command pattern: Join / Answer / Leave / StartGame
│   │   ├── game_engine.py     the state machine LOBBY -> QUESTION -> SCORING -> GAME_OVER
│   │   ├── question_manager.py  random questions, no repeats
│   │   └── score_engine.py    points by correctness and speed
│   ├── client/                MVC
│   │   ├── network_client.py  socket + reader thread + inbox queue   (Model)
│   │   ├── controllers/       messages -> screens, clicks -> messages (Controller)
│   │   └── views/             Tkinter screens only                    (View)
│   ├── admin/                 question management, CSV import, game history
│   ├── database/              SQLite: schema and repositories
│   └── utils/                 logging
│
├── data/questions_seed.csv    25 starter questions to import
├── tests/                     unit tests — some already written for you
└── docs/                      UML and the map to the project book
```

---

## Work order

`TASKS.md` is the most important document here: seven stages, each with the files to touch,
what to implement, and how to know the stage is finished. **Work in order.** Every stage assumes
the previous one works.

One tip: at the end of every stage do `git commit`. When something breaks — and something
always breaks — you can go back to a point that worked.

---

## Design patterns in the system

| Pattern | Where | Why |
|---|---|---|
| Client–Server, authoritative server | `server/` vs. `client/` | one source of truth for the game state |
| State machine | `GameEngine` | every message is legal only in some states |
| Command | `server/commands.py` | an action is an object; rules live in one place; replay |
| MVC | `client/` | screens know nothing about sockets or rules |
| Repository | `database/repositories.py` | SQL in one place only |
| Singleton | `Database` | one connection factory |
| Factory | `build_command()` | message -> Command object |
| Producer/Consumer | `NetworkClient.inbox` | the reader thread never touches Tkinter |

These are the chapters you will have to explain in the defense — make sure you understand why
each one is there.
