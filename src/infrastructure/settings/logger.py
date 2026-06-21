import logging
import sys

COLORS = {"DEBUG": "\033[36m", "INFO": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m", "CRITICAL": "\033[91m", "RESET": "\033[0m"}


class F(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{COLORS.get(record.levelname, COLORS['RESET'])}{record.levelname}{COLORS['RESET']}"
        return super().format(record)


def setup_logger(name: str = "app") -> logging.Logger:
    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG)

    if not l.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(F("%(levelname)s: %(message)s"))
        l.addHandler(h)

    return l
