import requests
from hermes_lite.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram(msg: str) -> None:
    if TELEGRAM_BOT_TOKEN is None or TELEGRAM_CHAT_ID is None:
        raise ValueError("Telegram credentials not set")
    url = API_URL.format(token=TELEGRAM_BOT_TOKEN)
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    resp = requests.post(url, data=data, timeout=10)
    resp.raise_for_status()
