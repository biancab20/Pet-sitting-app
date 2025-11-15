from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pet import Pet
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[AppointmentOut])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).order_by(Appointment.date, Appointment.start_time).all()


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    # 1) Ensure pet exists
    pet = db.query(Pet).filter(Pet.id == payload.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # 2) Optional: prevent overlapping appointments for same pet on same day
    _ensure_no_overlap(db, payload)

    new_appointment = Appointment(
        pet_id=payload.pet_id,
        sitter_name=payload.sitter_name,
        date=payload.date,
        start_time=payload.start_time,
        duration_minutes=payload.duration_minutes,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return


def _ensure_no_overlap(db: Session, payload: AppointmentCreate):
    """
    Simple overlap check:
    For the same pet & same date, (start_time, end_time) intervals must not overlap.
    """
    # Compute new appointment time window
    start_dt = datetime.combine(payload.date, payload.start_time)
    end_dt = start_dt + timedelta(minutes=payload.duration_minutes)

    existing = (
        db.query(Appointment)
        .filter(
            Appointment.pet_id == payload.pet_id,
            Appointment.date == payload.date,
        )
        .all()
    )

    for appt in existing:
        appt_start = datetime.combine(appt.date, appt.start_time)
        appt_end = appt_start + timedelta(minutes=appt.duration_minutes)

        # overlaps if not (new ends before existing starts OR new starts after existing ends)
        if not (end_dt <= appt_start or start_dt >= appt_end):
            raise HTTPException(
                status_code=400,
                detail="Appointment overlaps with an existing one for this pet on the same day.",
            )
