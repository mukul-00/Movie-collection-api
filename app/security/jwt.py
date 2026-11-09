from datetime import datetime, timedelta, timezone
from jose import jwt

from app.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode["exp"] = expire

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
