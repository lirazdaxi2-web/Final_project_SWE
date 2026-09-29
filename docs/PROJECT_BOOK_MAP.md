# Where each chapter of the project book comes from

| Project-book chapter | Source |
|---|---|
| 1. The approved proposal | `../הצעת_פרויקט/הצעת_פרויקט_05_LanGame_לירז_דקסה.docx` |
| 2. Introduction and background | Proposal §1–3, expanded |
| 3. Goals | Proposal §2 |
| 4. Challenges | Proposal §9 (SWOT: weaknesses/threats) + the bugs you logged in `TASKS.md` |
| 5. Success metrics | Proposal §10 vs. your measured numbers (server log, load test, pytest) |
| 6. Theoretical background | Proposal §3 + bibliography (§13): TCP vs UDP, client-server, threads, state machines |
| 7. Existing solutions | Kahoot, Quizizz, Blooket — compare: needs internet, cost, control over questions |
| 8–9. Alternatives and choice | TCP vs UDP; thread-per-client vs `selectors`/asyncio; JSON vs binary; Tkinter vs web |
| 10. System specification | Functional / non-functional requirements; `config.py` is the constraints list |
| 11. Architecture | `docs/UML.md` §5 + the folder tree in `README.md` |
| 12. UML | `docs/UML.md` |
| 13. Database | `langame/database/db.py` → `SCHEMA` + ERD |
| 14. Design patterns | Command, State machine, MVC, Repository, Singleton, Factory, Producer/Consumer — table in `README.md` |
| 15. Algorithms / protocol | `protocol.py` (framing), `score_engine.py` (formula), `game_engine.py` (state transitions) |
| 16. Network chapter | Wireshark capture of a round: handshake, JSON payloads, ACKs, port numbers |
| 17. User interface | Screenshots of the five client screens + admin |
| 18. Tests | `tests/` + `pytest -v` output + the 8-player load test |
| 19. Results | Latency table, load test, question statistics (`question_stats`) |
| 20. Conclusions and future work | Proposal §12 + what you actually learned |
| 21. Bibliography | Proposal §13 plus every source you used |

Rule of thumb: every number in the book comes from a file produced by a real run on your machine.
