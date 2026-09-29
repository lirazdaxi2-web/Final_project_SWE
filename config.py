"""
Central configuration for LanGame.

Every tunable value lives here so no magic numbers are scattered around the
code. This file is complete - change it only to tune the game later.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Paths ───────────────────────────────────────────────────────────
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
DATABASE_PATH = os.path.join(BASE_DIR, "langame.db")
QUESTIONS_CSV = os.path.join(DATA_DIR, "questions_seed.csv")

# ── Network ─────────────────────────────────────────────────────────
SERVER_HOST = "0.0.0.0"          # listen on every interface of this machine
SERVER_PORT = 5050
CLIENT_DEFAULT_HOST = "127.0.0.1"
ENCODING = "utf-8"
MESSAGE_DELIMITER = "\n"         # one JSON object per line (see protocol.py)
RECV_BUFFER_SIZE = 4096
MAX_MESSAGE_BYTES = 64 * 1024    # anything bigger is treated as an attack / bug
SOCKET_TIMEOUT_SECONDS = 1.0     # lets threads notice a shutdown request

# ── Game rules ──────────────────────────────────────────────────────
MIN_PLAYERS = 2
MAX_PLAYERS = 8
QUESTIONS_PER_GAME = 10
QUESTION_TIME_LIMIT = 15.0       # seconds
SECONDS_BETWEEN_QUESTIONS = 4.0  # results are shown this long
LOBBY_COUNTDOWN_SECONDS = 5
MAX_POINTS = 1000
MIN_POINTS_CORRECT = 100         # a correct answer never scores less than this
PLAYER_NAME_MAX_LENGTH = 16

# ── Admin defaults ──────────────────────────────────────────────────
DEFAULT_CATEGORY = "general"
DIFFICULTY_LEVELS = (1, 2, 3)
