from fastapi import Cookie, Depends, HTTPException, status

from app.core.security import hash_token
from app.core.settings import settings
from app.db.mongo import get_db


async def current_user(
    db=Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing session")
    token_hash = hash_token(session_token)
    session = await db.sessions.find_one({"tokenHash": token_hash})
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    user = await db.users.find_one({"_id": session["userId"]})
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
