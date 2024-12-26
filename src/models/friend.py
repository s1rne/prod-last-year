from typing import Any, Dict

from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import mapped_column

from db.session import Base


class Friend(Base):
    __tablename__ = "friends"
    
    id = mapped_column(BigInteger, primary_key=True)
    inviter_id = mapped_column(BigInteger)
    invitee_id = mapped_column(BigInteger)

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "inviter_id": self.inviter_id,
                "invitee_id": self.invitee_id
            }
        except Exception:
            return None
