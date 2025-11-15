from datetime import date, time, datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AppointmentBase(BaseModel):
    pet_id: int
    sitter_name: str = Field(..., min_length=1, max_length=100)
    date: date
    start_time: time
    duration_minutes: int = Field(..., gt=0, le=24 * 60)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
