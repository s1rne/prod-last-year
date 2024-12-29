from typing import Any, Dict
from sqlalchemy import DateTime, Integer, String, ARRAY, func, select
from sqlalchemy.orm import mapped_column

from db.session import Base
from utils.utils import generate_uuid
from db.session import Base, async_session


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    user_id = mapped_column(Integer)
    content = mapped_column(String)
    tags = mapped_column(ARRAY(String))
    createdAt = mapped_column(DateTime(timezone=True), default=func.now())

    async def to_dict(self) -> Dict[str, Any] | None:
        try:
            reactions = await self.get_reactions()
            return {
                "id": self.id,
                "user_id": self.user_id,
                "content": self.content,
                "tags": self.tags,
                "createdAt": self.createdAt.isoformat() + 'Z',
                "likesCount": reactions.count(1),
                "dislikesCount": reactions.count(-1),
            }
        except Exception:
            return None
    
    async def get_reactions(self) -> Dict[str, Any]:
        async with async_session() as session:
            reactions = await session.scalars(select(PostReaction).where(PostReaction.post_id == self.id))
            return [int(reaction.reaction) for reaction in reactions]


class PostReaction(Base):
    __tablename__ = "posts_reactions"

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    post_id = mapped_column(String)
    user_id = mapped_column(Integer)
    reaction = mapped_column(Integer)
