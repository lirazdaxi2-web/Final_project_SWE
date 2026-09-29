# UML diagrams required

Draw them **after** stage 6 works so they describe the real code. Tool: draw.io or PlantUML.

## 1. Use Case Diagram

Actors: **Player**, **Host** (a player with one extra action), **Teacher/Admin**.

- Player: connect, join lobby, answer a question, see result, see leaderboard, leave
- Host: start the game
- Admin: add / edit / delete question, import CSV, view game history, view question statistics
- System (secondary actor): time limit expires

## 2. Class Diagram

Must show:

- **Inheritance**: `Command` ← `JoinCommand`, `AnswerCommand`, `LeaveCommand`, `StartGameCommand`
- **Composition**: `GameServer` ◆— `GameEngine` ◆— `QuestionManager`, `ScoreEngine`; `GameServer` ◆— `ClientHandler` (0..8)
- **Singleton**: `Database`
- **Repository**: `QuestionRepository`, `GameRepository` → `Database`
- **Entities**: `Question`, `Player`, `AnswerRecord`, `LeaderboardEntry`, `GameState` (enum)
- **Client MVC**: `ClientController` → `NetworkClient` (Model) and → `MainWindow` + views (View);
  views have no arrow to anything in `common.protocol` or `server`

## 3. State Diagram — `GameEngine`

```
[*] --> LOBBY
LOBBY --> QUESTION    : StartGameCommand [players >= MIN] / prepare questions, COUNTDOWN
QUESTION --> SCORING  : timer expires | all connected answered / score_round, RESULT, LEADERBOARD
SCORING --> QUESTION  : more questions / next_question
SCORING --> GAME_OVER : last question / save_game, GAME_OVER
GAME_OVER --> LOBBY   : reset
LOBBY --> LOBBY       : JoinCommand, LeaveCommand
QUESTION --> QUESTION : AnswerCommand [valid] / record
```

This is the diagram examiners look at first in a networking project. Every arrow = one method.

## 4. Sequence Diagram — one question round

```
Engine -> Broadcaster: QUESTION (t0 = monotonic())
Broadcaster -> Client A, B, C: QUESTION
Client A -> HandlerA: ANSWER (choice 2)
HandlerA -> Engine: execute(AnswerCommand)      [lock]
Engine -> Engine: record_answer (t = now - t0)
Client B -> HandlerB: ANSWER (choice 0)
HandlerB -> Engine: execute(AnswerCommand)      [lock]
Timer -> Engine: close_question
Engine -> ScoreEngine: score_round
Engine -> Broadcaster: RESULT, LEADERBOARD
Broadcaster -> Client A, B, C: RESULT, LEADERBOARD
```

## 5. Deployment / Network Diagram

One server machine (IP, port 5050), N client machines, one switch / Wi-Fi access point;
TCP connections drawn as lines. Add the admin tool on the server machine (same DB file).

## 6. ERD

Four tables from `langame/database/db.py` → `SCHEMA`: `questions`, `games` 1→* `players`,
`games` 1→* `answers`, `players` 1→* `answers`, `questions` 1→* `answers`. Mark the `ON DELETE CASCADE` edges.
