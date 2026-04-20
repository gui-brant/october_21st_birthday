from pydantic import BaseModel, EmailStr, Field


class SignUpInput(BaseModel):
    first_name: str = Field(min_length=1, max_length=60)
    last_name: str = Field(min_length=1, max_length=60)
    age: int = Field(ge=1, le=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    remember_me: bool = False


class OTPVerifyInput(BaseModel):
    email: EmailStr
    otp_code: str = Field(min_length=6, max_length=6)


class OTPChallengeResponse(BaseModel):
    message: str
    otp_sent: bool = True


class SessionResponse(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    current_level: int
    current_exp: float
