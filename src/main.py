
"""Main process that runs the directory monitor and optional bot."""

import os
import threading
import time
from pathlib import Path

from .bot import run as run_bot
from .modulos.watchdog_module import build_monitor


def main() -> None:
    """Start the monitoring service and the Telegram bot."""
    base = Path(__file__).resolve().parent.parent
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    monitor = build_monitor(base, token, chat_id)

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()


if __name__ == "__main__":
    main()
