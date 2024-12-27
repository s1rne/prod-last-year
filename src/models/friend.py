import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, String, func, select
from sqlalchemy.orm import mapped_column

from db.session import Base, async_session
from models.user import User
from utils.utils import generate_uuid


class Friend(Base):
    __tablename__ = "friends"

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    inviter_id = mapped_column(String)
    invitee_id = mapped_column(String)
    addedAt = mapped_column(DateTime(timezone=True), default=func.now())

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "inviter_id": self.inviter_id,
                "invitee_id": self.invitee_id,
                "addedAt": self.addedAt.isoformat() + 'Z'
            }
        except Exception:
            return None

    async def get_invitee(self) -> User:
        async with async_session() as session:
            invitee = await session.scalar(select(User).where(User.id == self.invitee_id))
            return invitee
        
    async def friend_dict(self) -> Dict[str, Any]:
        invitee = await self.get_invitee()
        return {
            "login": invitee.login,
            "addedAt": self.addedAt.isoformat() + 'Z'
        }
