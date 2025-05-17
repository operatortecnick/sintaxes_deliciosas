import logging
from pathlib import Path


def setup_logging(log_file: Path, level: int = logging.INFO) -> None:
    """Configura logging em arquivo e console."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    fmt = '%(asctime)s [%(levelname)s] %(message)s'
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
    logging.basicConfig(level=level, format=fmt, handlers=handlers)
