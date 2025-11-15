from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.models.appointment import Appointment
from datetime import date, time, timedelta, datetime


def seed_data(db: Session):
    # ---- Seed Pets ----
    if db.query(Pet).count() == 0:
        print("🌱 Seeding initial pets...")

        pets = [
            Pet(name="Bella", breed="Labrador Retriever", size="large", birthdate=date(2018, 6, 12)),
            Pet(name="Milo", breed="Beagle", size="medium", birthdate=date(2020, 2, 8)),
            Pet(name="Luna", breed="Pomeranian", size="small", birthdate=date(2021, 10, 22)),
            Pet(name="Rex", breed="German Shepherd", size="large", birthdate=date(2024, 2, 18)),
            Pet(name="Daisy", breed="Beagle", size="medium", birthdate=date(2021, 2, 8)),
            Pet(name="Lucy", breed="Border Collie", size="medium", birthdate=date(2023, 12, 22)),
            Pet(name="Oliver", breed="Harrier", size="small", birthdate=date(2025, 2, 8)),
        ]

        db.add_all(pets)
        db.commit()
        print("🌱 Pets seeded!")
    else:
        print("🌱 Pets already seeded, skipping...")

    # ---- Seed Appointments ----
    if db.query(Appointment).count() > 0:
        print("🌱 Appointments already seeded, skipping...")
        return

    print("🌱 Seeding appointments...")

    pets = db.query(Pet).all()
    if not pets:
        print("❌ No pets found, skipping appointment seeding.")
        return

    # Helpers
    today = date.today()

    appointments = [
        # ---- Future Appointments ----
        Appointment(
            pet_id=pets[5].id,
            sitter_name="Alice Johnson",
            date=today + timedelta(days=2),
            start_time=time(10, 0, 0),
            duration_minutes=60,
        ),
        Appointment(
            pet_id=pets[1].id,
            sitter_name="Mark Benson",
            date=today + timedelta(days=5),
            start_time=time(14, 30, 0),
            duration_minutes=45,
        ),
        Appointment(
            pet_id=pets[2].id,
            sitter_name="Emily Clark",
            date=today + timedelta(days=10),
            start_time=time(9, 0, 0),
            duration_minutes=30,
        ),

        # ---- Past Appointments ----
        Appointment(
            pet_id=pets[3].id,
            sitter_name="John Doe",
            date=today - timedelta(days=3),
            start_time=time(13, 0, 0),
            duration_minutes=90,
        ),
        Appointment(
            pet_id=pets[4].id,
            sitter_name="Sarah Miller",
            date=today - timedelta(days=10),
            start_time=time(16, 15, 0),
            duration_minutes=60,
        ),
    ]

    db.add_all(appointments)
    db.commit()
    print("🌱 Appointment seeding completed!")
