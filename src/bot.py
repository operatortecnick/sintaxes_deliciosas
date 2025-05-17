import os
import requests
import os
import requests
import time
import logging

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
OFFSET = 0


def send_message(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        logging.warning('Telegram não configurado.')
        return
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})


def handle_update(update: dict) -> None:
    message = update.get('message', {}).get('text', '')
    if message == '/start':
        send_message('Bot iniciado!')
    elif message == '/print':
        send_message('Comando /print recebido.')


def bot_loop(stop_event) -> None:
    global OFFSET
    while not stop_event.is_set():
        url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
        resp = requests.get(url, params={'timeout': 30, 'offset': OFFSET + 1})
        if resp.ok:
            for update in resp.json().get('result', []):
                OFFSET = update['update_id']
                handle_update(update)
        time.sleep(1)
