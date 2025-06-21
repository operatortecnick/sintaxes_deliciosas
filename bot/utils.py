import random
import string
from typing import Iterable

DEFAULT_NAMES = [
    "Lucas", "Bruna", "Caio", "Renata", "Jo\u00e3o", "Marina"
]

DEFAULT_SURNAMES = [
    "Silva", "Oliveira", "Costa", "Ferreira", "Lima"
]

def random_choice(values: Iterable[str]) -> str:
    seq = list(values)
    return random.choice(seq)

def generate_name(first_names: Iterable[str] = DEFAULT_NAMES, surnames: Iterable[str] = DEFAULT_SURNAMES) -> str:
    return f"{random_choice(first_names)} {random_choice(surnames)}"

def generate_username(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_password() -> str:
    return "SenhaForte123!"
