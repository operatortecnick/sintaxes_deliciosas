
"""Monitoring utilities based on watchdog."""

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .telegram_module import send_message
from ..funcoes.utils import setup_logger


class WatchHandler(FileSystemEventHandler):
    """Handle file system events and send notifications."""

    def __init__(self, logger, token: str | None = None, chat_id: str | None = None) -> None:
        super().__init__()
        self.logger = logger
        self.token = token
        self.chat_id = chat_id

    def on_created(self, event):  # type: ignore[override]
        if event.is_directory:
            return
        self.logger.info("Arquivo criado: %s", event.src_path)
        if self.token and self.chat_id:
            send_message(self.token, self.chat_id, f"Criado: {event.src_path}")

    def on_modified(self, event):  # type: ignore[override]
        if event.is_directory:
            return
        self.logger.info("Arquivo modificado: %s", event.src_path)


class Monitor:
    """Monitor a folder for changes."""

    def __init__(self, folder: Path, logger, token: str | None = None, chat_id: str | None = None) -> None:
        self.folder = folder
        self.handler = WatchHandler(logger, token, chat_id)
        self.observer = Observer()

    def start(self):
        """Start watching."""
        self.observer.schedule(self.handler, str(self.folder), recursive=True)
        self.observer.start()

    def stop(self):
        """Stop watching."""
        self.observer.stop()
        self.observer.join()


def build_monitor(base: Path, token: str | None = None, chat_id: str | None = None) -> Monitor:
    """Create a Monitor instance for the project."""
    log_file = base / "src" / "logs" / "registro.log"
    logger = setup_logger(log_file)
    folder = base / "monitora"
    folder.mkdir(exist_ok=True)
    return Monitor(folder, logger, token, chat_id)
