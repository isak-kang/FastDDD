import logging
import sys

DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def setup_logging(log_level: str = "INFO") -> None:
    level = _resolve_log_level(log_level)
    root_logger = logging.getLogger()

    root_logger.setLevel(level)
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))

    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def _resolve_log_level(log_level: str) -> int:
    return getattr(logging, log_level.upper(), logging.INFO)
