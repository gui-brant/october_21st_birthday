from datetime import UTC, datetime

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from app.core.security import (
    expires_at,
    hash_password,
    hash_token,
    make_otp_code,
    make_session_token,
    verify_password,
)
from app.core.settings import settings
from app.db.mongo import get_db
from app.schemas.auth import (
    LoginInput,
    OTPChallengeResponse,
    OTPVerifyInput,
    SessionResponse,
    SignUpInput,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=OTPChallengeResponse)
async def signup(payload: SignUpInput, db=Depends(get_db)):
    email = payload.email.lower().strip()
    existing = await db.users.find_one({"email": email})
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already used")
    now = datetime.now(UTC)
    user_doc = {
        "email": email,
        "passwordHash": hash_password(payload.password),
        "firstName": payload.first_name.strip(),
        "lastName": payload.last_name.strip(),
        "age": payload.age,
        "timezone": "UTC",
        "currentLevel": 1,
        "currentExp": 0.0,
        "totalExpEarned": 0.0,
        "googleAccessToken": None,
        "googleRefreshToken": None,
        "googleTokenExpiry": None,
        "sessionTimeoutMinutes": settings.default_session_timeout_minutes,
        "listingStyle": "numbered",
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.users.insert_one(user_doc)
    code = make_otp_code()
    await db.otp_tokens.insert_one(
        {
            "userId": result.inserted_id,
            "codeHash": hash_password(code),
            "attempts": 0,
            "locked": False,
            "expiresAt": expires_at(settings.otp_expiry_minutes),
        }
    )
    return OTPChallengeResponse(message="Signup accepted. OTP challenge issued.")


@router.post("/login", response_model=OTPChallengeResponse)
async def login(payload: LoginInput, db=Depends(get_db)):
    email = payload.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if user is None or not verify_password(payload.password, user["passwordHash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    code = make_otp_code()
    await db.otp_tokens.delete_many({"userId": user["_id"]})
    await db.otp_tokens.insert_one(
        {
            "userId": user["_id"],
            "codeHash": hash_password(code),
            "attempts": 0,
            "locked": False,
            "expiresAt": expires_at(settings.otp_expiry_minutes),
            "rememberMe": payload.remember_me,
        }
    )
    return OTPChallengeResponse(message="Credentials verified. OTP challenge issued.")


@router.post("/otp/verify", response_model=SessionResponse)
async def verify_otp(payload: OTPVerifyInput, response: Response, db=Depends(get_db)):
    user = await db.users.find_one({"email": payload.email.lower().strip()})
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid challenge")
    otp_doc = await db.otp_tokens.find_one({"userId": user["_id"]})
    if otp_doc is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP missing or expired")
    if otp_doc.get("locked"):
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="OTP challenge locked")
    if datetime.now(UTC) > otp_doc["expiresAt"]:
        await db.otp_tokens.delete_one({"_id": otp_doc["_id"]})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP expired")
    if not verify_password(payload.otp_code, otp_doc["codeHash"]):
        attempts = int(otp_doc.get("attempts", 0)) + 1
        locked = attempts >= settings.otp_max_attempts
        await db.otp_tokens.update_one(
            {"_id": otp_doc["_id"]},
            {"$set": {"attempts": attempts, "locked": locked}},
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")

    raw_session = make_session_token()
    session_hash = hash_token(raw_session)
    timeout = user.get("sessionTimeoutMinutes", settings.default_session_timeout_minutes)
    await db.sessions.insert_one(
        {
            "userId": user["_id"],
            "tokenHash": session_hash,
            "userAgent": None,
            "ip": None,
            "expiresAt": expires_at(timeout if timeout > 0 else 365 * 24 * 60),
        }
    )
    await db.otp_tokens.delete_one({"_id": otp_doc["_id"]})
    response.set_cookie(
        key=settings.session_cookie_name,
        value=raw_session,
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return SessionResponse(
        user_id=str(user["_id"]),
        first_name=user["firstName"],
        last_name=user["lastName"],
        current_level=user["currentLevel"],
        current_exp=user["currentExp"],
    )


@router.post("/logout")
async def logout(
    response: Response,
    db=Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
):
    if session_token:
        await db.sessions.delete_one({"tokenHash": hash_token(session_token)})
    response.delete_cookie(settings.session_cookie_name)
    return {"message": "Logged out"}
