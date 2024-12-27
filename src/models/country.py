from typing import Any, Dict

from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from db.session import Base
from utils.utils import generate_uuid


class Country(Base):
    __tablename__ = "countries"

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    name = mapped_column(String)
    alpha2 = mapped_column(String)
    alpha3 = mapped_column(String)
    region = mapped_column(String)

    def to_dict(self) -> Dict[str, Any] | None:
        try:
            return {
                "name": self.name,
                "alpha2": self.alpha2,
                "alpha3": self.alpha3,
                "region": self.region
            }
        except Exception:
            return None

