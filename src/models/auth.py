from typing import Any, Dict

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column

from db.session import Base
from utils.utils import generate_uuid


class Session(Base):
    __tablename__ = "sessions"
    
    id = mapped_column(String, default=generate_uuid, primary_key=True)
    user_id = mapped_column(String)
    token = mapped_column(String)
    last_online_time = mapped_column(BigInteger)
    

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "user_id": self.user_id,
                "token": self.token,
                "last_online_time": self.last_online_time
            }
        except Exception:
            return None
