
"""Utility helpers for the project."""

from pathlib import Path
import logging
from datetime import datetime


def setup_logger(log_file: Path) -> logging.Logger:
    """Return a logger that writes to *log_file*."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("sintaxes")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def capture_screenshot(path: Path) -> None:
    """Try to capture the screen and save it to *path*."""
    try:
        from PIL import ImageGrab
    except Exception:
        return

    image = ImageGrab.grab()
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def timestamp() -> str:
    """Return current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
