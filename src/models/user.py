from typing import Any, Dict

from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import mapped_column

from db.session import Base


class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(BigInteger, primary_key=True)
    login = mapped_column(String)
    email = mapped_column(String)
    passwordHash = mapped_column(String)
    countryCode = mapped_column(String)
    isPublic = mapped_column(Boolean)
    phone = mapped_column(String, nullable=True)
    image = mapped_column(String, nullable=True)

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "login": self.login,
                "email": self.email,
                "passwordHash": self.passwordHash,
                "countryCode": self.countryCode,
                "isPublic": self.isPublic,
                "phone": self.phone,
                "image": self.image
            }
        except Exception:
            return None
