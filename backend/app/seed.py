from sqlalchemy.orm import Session
from app.models.pet import Pet
from datetime import date

def seed_data(db: Session):
    # Check if pets already exist (avoid duplicates)
    if db.query(Pet).count() > 0:
        print("🌱 Database already seeded, skipping...")
        return

    print("🌱 Seeding initial pets...")

    pets = [
        Pet(
            name="Bella",
            breed="Labrador Retriever",
            size="large",
            birthdate=date(2018, 6, 12)
        ),
        Pet(
            name="Milo",
            breed="Beagle",
            size="medium",
            birthdate=date(2020, 2, 8)
        ),
        Pet(
            name="Luna",
            breed="Pomeranian",
            size="small",
            birthdate=date(2021, 10, 22)
        ),
        Pet(
            name="Rex",
            breed="German Shepherd",
            size="large",
            birthdate=date(2024, 2, 18)
        ),
        Pet(
            name="Daisy",
            breed="Beagle",
            size="medium",
            birthdate=date(2021, 2, 8)
        ),
        Pet(
            name="Lucy",
            breed="Border Collie",
            size="medium",
            birthdate=date(2023, 12, 22)
        ),
        Pet(
            name="Oliver",
            breed="Harrier",
            size="small",
            birthdate=date(2025, 2, 8)
        ),
    ]

    db.add_all(pets)
    db.commit()

    print("🌱 Seed completed!")
