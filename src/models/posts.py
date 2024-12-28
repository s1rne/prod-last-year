from typing import Any, Dict
from sqlalchemy import DateTime, Integer, String, ARRAY, func
from sqlalchemy.orm import mapped_column

from db.session import Base
from utils.utils import generate_uuid


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    user_id = mapped_column(Integer)
    content = mapped_column(String)
    tags = mapped_column(ARRAY(String))
    createdAt = mapped_column(DateTime(timezone=True), default=func.now())
    likesCount = mapped_column(Integer, default=0)
    dislikesCount = mapped_column(Integer, default=0)

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "id": self.id,
                "user_id": self.user_id,
                "content": self.content,
                "tags": self.tags,
                "createdAt": self.createdAt.isoformat() + 'Z',
                "likesCount": self.likesCount,
                "dislikesCount": self.dislikesCount
            }
        except Exception:
            return None
