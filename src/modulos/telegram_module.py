import os
import logging
import requests

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        logging.warning('Credenciais do Telegram ausentes.')
        return
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    resp = requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
    if not resp.ok:
        logging.error('Falha ao enviar mensagem: %s', resp.text)
