from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException, status

API_KEY_HEADER = "X-API-Key"
API_KEY = os.getenv("EAT_RIGHT_API_KEY", "dev-local-key")


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    provided = x_api_key or ""
    if not hmac.compare_digest(provided, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid API key. Provide it in {API_KEY_HEADER} header.",
        )
    return provided
