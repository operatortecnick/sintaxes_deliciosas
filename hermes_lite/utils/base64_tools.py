import base64


def encode_b64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def decode_b64(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception as exc:
        raise ValueError("Invalid base64 input") from exc
