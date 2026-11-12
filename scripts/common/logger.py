
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Common logging utility.
"""

import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_FOLDER = PROJECT_ROOT / "logs"

LOG_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_FOLDER / "data_generation.log"


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logger = logging.getLogger("fmcg_sales")

logger.setLevel(logging.INFO)

# Prevent messages from being duplicated by the root logger.
logger.propagate = False


# ============================================================
# LOG FORMAT
# ============================================================

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# ============================================================
# CONFIGURE HANDLERS
# ============================================================

if not logger.handlers:

    # File handler with log rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
