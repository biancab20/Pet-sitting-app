from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate, PetOut

router = APIRouter(prefix="/pets", tags=["Pets"])


# GET all pets
@router.get("/", response_model=list[PetOut])
def get_pets(db: Session = Depends(get_db)):
    return db.query(Pet).order_by(Pet.id).all()


# GET pet by ID
@router.get("/{pet_id}", response_model=PetOut)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


# CREATE pet
@router.post("/", response_model=PetOut, status_code=status.HTTP_201_CREATED)
def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    new_pet = Pet(**pet_data.dict())
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


# UPDATE pet
@router.put("/{pet_id}", response_model=PetOut)
def update_pet(pet_id: int, pet_data: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    for field, value in pet_data.dict(exclude_unset=True).items():
        setattr(pet, field, value)

    db.commit()
    db.refresh(pet)
    return pet


# DELETE pet
@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    db.delete(pet)
    db.commit()
    return
