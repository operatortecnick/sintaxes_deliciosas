import requests
from hermes_lite.config import LEAKCHECK_API_KEY

API_URL = "https://leakcheck.io/api"


def check_leak(query: str) -> dict:
    if LEAKCHECK_API_KEY is None:
        raise ValueError("LEAKCHECK_API_KEY not set")
    params = {
        "key": LEAKCHECK_API_KEY,
        "check": query,
        "type": "email",
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
