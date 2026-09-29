"""
Start a player client.

    python run_client.py                     # connects to 127.0.0.1:5050
    python run_client.py --host 192.168.1.20 --port 5050

Opens the Tkinter window: a connect screen, the lobby, then questions.
"""
import argparse
import tkinter as tk

import config
from langame.client.controllers.client_controller import ClientController


def parse_args():
    parser = argparse.ArgumentParser(description="LanGame player client")
    parser.add_argument("--host", type=str, default=config.CLIENT_DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=config.SERVER_PORT)
    return parser.parse_args()


def main():
    args = parse_args()
    root = tk.Tk()
    root.title("LanGame")
    root.minsize(720, 520)
    controller = ClientController(root, default_host=args.host, default_port=args.port)
    controller.start()
    root.mainloop()


if __name__ == "__main__":
    main()
