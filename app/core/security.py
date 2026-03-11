from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time

SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
TOKEN_EXPIRE_SECONDS = 60 * 60


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def get_password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"pbkdf2_sha256${_b64url_encode(salt)}${_b64url_encode(hashed)}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        _, salt, expected_hash = stored_hash.split("$", maxsplit=2)
    except ValueError:
        return False

    computed = hashlib.pbkdf2_hmac("sha256", password.encode(), _b64url_decode(salt), 200_000)
    return hmac.compare_digest(_b64url_encode(computed), expected_hash)


def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": int(time.time()) + TOKEN_EXPIRE_SECONDS,
    }
    payload_part = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signature = hmac.new(SECRET_KEY.encode(), payload_part.encode(), hashlib.sha256).digest()
    return f"{payload_part}.{_b64url_encode(signature)}"


def decode_access_token(token: str) -> str:
    try:
        payload_part, signature_part = token.split(".", maxsplit=1)
    except ValueError as exc:
        raise ValueError("Malformed token") from exc

    expected_sig = hmac.new(SECRET_KEY.encode(), payload_part.encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(_b64url_encode(expected_sig), signature_part):
        raise ValueError("Invalid token signature")

    payload = json.loads(_b64url_decode(payload_part).decode())
    if payload.get("exp", 0) < int(time.time()):
        raise ValueError("Token expired")

    subject = payload.get("sub")
    if not subject:
        raise ValueError("Token subject missing")
    return subject
