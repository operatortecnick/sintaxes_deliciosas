
"""Minimal helpers to interact with the Telegram Bot API."""

import requests


API_URL = "https://api.telegram.org/bot{token}/{method}"


def send_message(token: str, chat_id: str, text: str) -> None:
    """Send a text message using the Bot API."""
    url = API_URL.format(token=token, method="sendMessage")
    requests.post(url, json={"chat_id": chat_id, "text": text})


def send_photo(token: str, chat_id: str, path: str) -> None:
    """Send a photo to the chat."""
    url = API_URL.format(token=token, method="sendPhoto")
    with open(path, "rb") as photo:
        requests.post(url, files={"photo": photo}, data={"chat_id": chat_id})
