from pydantic import BaseModel


class UpdatePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str


class UpdateProfileRequest(BaseModel):
    email: str | None = None
    countryCode: str | None = None
    isPublic: bool | None = None
    phone: str | None = None
    image: str | None = None
