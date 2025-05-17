
"""Simple Telegram bot with a few commands."""

import os
import time
import requests
from pathlib import Path

from .modulos.telegram_module import send_message, send_photo
from .funcoes.utils import capture_screenshot


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"


def run() -> None:
    """Start polling Telegram for new messages."""
    if not TOKEN or not CHAT_ID:
        print("Telegram token or chat id not configured")
        return

    offset = 0
    while True:
        resp = requests.get(API_URL, params={"offset": offset, "timeout": 60})
        if resp.status_code != 200:
            time.sleep(5)
            continue
        data = resp.json().get("result", [])
        for update in data:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            text = message.get("text", "")
            if text == "/start":
                send_message(TOKEN, CHAT_ID, "Bot iniciado")
            elif text == "/print":
                path = Path(__file__).resolve().parent / "logs" / "screenshot.png"
                capture_screenshot(path)
                send_photo(TOKEN, CHAT_ID, str(path))


if __name__ == "__main__":
    run()
