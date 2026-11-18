import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def create_token(username: str) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not configured. Set it in your environment.")

    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "exp": now + timedelta(days=1),
        "iat": now,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not configured. Set it in your environment.")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")
