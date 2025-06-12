from hashlib import md5, sha256
from typing import Literal


def generate_hash(text: str, method: Literal["md5", "sha256"] = "md5") -> str:
    if method == "md5":
        return md5(text.encode()).hexdigest()
    if method == "sha256":
        return sha256(text.encode()).hexdigest()
    raise ValueError("Unsupported hash method.")
