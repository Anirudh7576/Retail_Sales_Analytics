"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Common logging utility.
"""

import logging
from pathlib import Path


# Project root
project_root = Path(__file__).resolve().parents[2]

# Log directory
log_folder = project_root / "logs"
log_folder.mkdir(parents=True, exist_ok=True)

# Log file
log_file = log_folder / "data_generation.log"


# Create logger
logger = logging.getLogger("retail_sales")

logger.setLevel(logging.INFO)


# Prevent duplicate handlers
if not logger.handlers:

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)