import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def configure_logging(level="INFO"):
    log = logging.getLogger()
    log.setLevel(level)
    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    log.addHandler(sh)
    fh = RotatingFileHandler(LOG_DIR/"bot.log", maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(fmt)
    log.addHandler(fh)
