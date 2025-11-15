from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal


PetSizeLiteral = Literal["small", "medium", "large"]


class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: str = Field(..., min_length=1, max_length=100)
    size: PetSizeLiteral
    birthdate: date


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    breed: Optional[str] = Field(None, min_length=1, max_length=100)
    size: Optional[PetSizeLiteral] = None
    birthdate: Optional[date] = None


class PetOut(PetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
