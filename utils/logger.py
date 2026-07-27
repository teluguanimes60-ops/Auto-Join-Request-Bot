import logging
import os
from logging.handlers import RotatingFileHandler

# ==========================================
# Log Directory
# ==========================================

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "bot.log")

# ==========================================
# Logger
# ==========================================

logger = logging.getLogger("AutoJoinBot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    "%d-%m-%Y %H:%M:%S",
)

# ==========================================
# File Handler
# ==========================================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)

# ==========================================
# Console Handler
# ==========================================

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# ==========================================
# Add Handlers
# ==========================================

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# ==========================================
# Helper Functions
# ==========================================

def info(message):
    logger.info(message)


def warning(message):
    logger.warning(message)


def error(message):
    logger.error(message)


def critical(message):
    logger.critical(message)


def exception(exc):
    logger.exception(exc)
