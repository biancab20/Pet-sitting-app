from sqlalchemy import Column, Integer, String, Date, DateTime, Enum
from datetime import datetime
import enum

from app.database import Base


class PetSize(str, enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    size = Column(Enum(PetSize), nullable=False)
    birthdate = Column(Date, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
