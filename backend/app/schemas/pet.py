from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional, Literal


PetSizeLiteral = Literal["small", "medium", "large"]
PetTypeLiteral = Literal["dog", "cat", "rabbit", "other"]


class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: str = Field(..., min_length=1, max_length=100)
    size: PetSizeLiteral
    birthdate: date

    pet_type: Optional[PetTypeLiteral] = None
    image_url: Optional[HttpUrl] = None

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

    pet_type: Optional[PetTypeLiteral] = None
    image_url: Optional[HttpUrl] = None


class PetOut(PetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
