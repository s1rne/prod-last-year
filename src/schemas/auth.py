from pydantic import BaseModel


class RegisterRequest(BaseModel):
    login: str
    password: str
    email: str
    countryCode: str
    isPublic: bool
    phone: str | None = None
    image: str | None = None


class SignInRequest(BaseModel):
    login: str
    password: str
