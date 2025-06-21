import requests
import time
import random
import string
from typing import Optional

class MailTM:
    """Simple wrapper around the mail.tm temporary email API."""

    def __init__(self, session: Optional[requests.Session] = None, password: str = "BotInsta123!"):
        self.session = session or requests.Session()
        self.base_url = "https://api.mail.tm"
        self.domain = self._get_domain()
        self.password = password
        self.address, self.token = self._register_account()

    def _get_domain(self) -> str:
        res = self.session.get(f"{self.base_url}/domains")
        res.raise_for_status()
        return res.json()['hydra:member'][0]['domain']

    def _generate_username(self) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    def _register_account(self):
        username = self._generate_username()
        email = f"{username}@{self.domain}"
        self.session.post(f"{self.base_url}/accounts", json={"address": email, "password": self.password})
        res = self.session.post(f"{self.base_url}/token", json={"address": email, "password": self.password})
        res.raise_for_status()
        token = res.json()['token']
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return email, token

    def get_last_code(self, timeout: int = 90, interval: int = 2) -> Optional[str]:
        """Poll the inbox looking for numeric code in the latest message."""
        for _ in range(max(1, timeout)):
            res = self.session.get(f"{self.base_url}/messages")
            res.raise_for_status()
            data = res.json()
            if data.get('hydra:member'):
                body = data['hydra:member'][0].get('text', '')
                code = ''.join(filter(str.isdigit, body))
                if code:
                    return code
            time.sleep(max(1, interval))
        return None
