import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def make_otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def make_session_token() -> str:
    return secrets.token_urlsafe(48)


def utc_now() -> datetime:
    return datetime.now(UTC)


def expires_at(minutes: int) -> datetime:
    return utc_now() + timedelta(minutes=minutes)
