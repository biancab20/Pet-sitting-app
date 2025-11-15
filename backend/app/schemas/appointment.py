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
    @field_validator("date")
    @classmethod
    def date_cannot_be_in_past(cls, value: date) -> date:
        from datetime import date as _date
        if value < _date.today():
            raise ValueError("Appointment date cannot be in the past")
        return value


class AppointmentOut(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
