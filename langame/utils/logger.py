"""Logging setup - complete. The server log is your best friend when debugging threads."""
import logging


def setup_logging(path: str, level: int = logging.INFO) -> None:
    fmt = "%(asctime)s %(levelname)-7s [%(threadName)s] %(name)s: %(message)s"
    logging.basicConfig(level=level, format=fmt,
                        handlers=[logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler()])
