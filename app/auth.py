import secrets
from fastapi import Header, HTTPException
from .config import API_KEY

def require_api_key(x_api_key: str | None = Header(default=None)):
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Valid X-API-Key required")
    return True
