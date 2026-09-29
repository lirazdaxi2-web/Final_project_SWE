"""
Start the LanGame server.

    python run_server.py
    python run_server.py --port 6000 --questions 15 --category science

The server prints the IP addresses players should type into their client and
then runs until Ctrl+C. Every player connection gets its own thread; the game
itself is driven by GameEngine (a state machine) - see docs/UML.md.
"""
import argparse
import logging
import os
import socket

import config
from langame.database.db import Database
from langame.server.game_server import GameServer
from langame.utils.logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description="LanGame trivia server")
    parser.add_argument("--port", type=int, default=config.SERVER_PORT)
    parser.add_argument("--questions", type=int, default=config.QUESTIONS_PER_GAME)
    parser.add_argument("--time-limit", type=float, default=config.QUESTION_TIME_LIMIT)
    parser.add_argument("--category", type=str, default=None, help="restrict questions to one category")
    return parser.parse_args()


def print_local_addresses(port: int):
    """
    TODO stage 2: print every IPv4 address of this machine so players know what
    to type. Hint: socket.gethostbyname_ex(socket.gethostname())[2], plus
    127.0.0.1 for players on the same computer.
    """
    raise NotImplementedError


def main():
    args = parse_args()
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    setup_logging(os.path.join(config.LOGS_DIR, "server.log"))
    logging.getLogger("langame").info("starting server on port %s", args.port)

    Database().initialize_schema()
    print_local_addresses(args.port)

    server = GameServer(port=args.port, questions_per_game=args.questions,
                        time_limit=args.time_limit, category=args.category)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
