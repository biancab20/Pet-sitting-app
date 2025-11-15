from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


PetSizeLiteral = Literal["small", "medium", "large"]


class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: str = Field(..., min_length=1, max_length=100)
    size: PetSizeLiteral
    birthdate: date

    @field_validator("birthdate")
    def no_future_birthdate(cls, value):
        if value > date.today():
            raise ValueError("Birthdate cannot be in the future")
        return value

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
