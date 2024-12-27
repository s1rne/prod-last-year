import hashlib
import uuid

from config import RANDOM_SECRET
from db import tools
from schemas.auth import RegisterRequest
from schemas.me import UpdateProfileRequest


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode() + RANDOM_SECRET.encode()).hexdigest()


class ValidationUserData:
    def validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        return True

    def validate_email(self, email: str) -> bool:
        if not "@" in email:
            return False
        return True

    async def validate_country(self, countryCode: str) -> bool:
        if not await tools.get_country(countryCode):
            return False
        return True

    def validate_phone(self, phone: str) -> bool:
        if phone and (not phone.startswith("+") or len(phone) > 15):
            return False
        return True

    def validate_image(self, image: str) -> bool:
        if image and (not image.startswith("http") or len(image) > 50):
            return False
        return True

    async def vaidate_register_request(self, request: RegisterRequest) -> bool:
        if not self.validate_password(request.password):
            return False
        if not self.validate_email(request.email):
            return False
        if not await self.validate_country(request.countryCode):
            return False
        if not self.validate_phone(request.phone):
            return False
        if not self.validate_image(request.image):
            return False
        return True

    async def validate_update_profile_request(self, request: UpdateProfileRequest) -> bool:
        if request.email and not self.validate_email(request.email):
            return False
        if request.countryCode and not await self.validate_country(request.countryCode):
            return False
        if request.isPublic and not isinstance(request.isPublic, bool):
            return False
        if request.phone and not self.validate_phone(request.phone):
            return False
        if request.image and not self.validate_image(request.image):
            return False
        return True


validation_user_data = ValidationUserData()


def collect_user_data(user: dict):
    content = {
        "login": user["login"],
        "email": user["email"],
        "countryCode": user["countryCode"],
        "isPublic": user["isPublic"],
    }
    if user["image"] is not None:
        content["image"] = user["image"]
    if user["phone"] is not None:
        content["phone"] = user["phone"]
    return content


def generate_uuid():
    return str(uuid.uuid4())
