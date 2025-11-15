from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app import models
from app.routes.pet_routes import router as pets_router
from app.routes.appointment_routes import router as appointments_router
from app.seed import seed_data

app = FastAPI(title="Pet Sitting API")

origins = [
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# --- Run seed on startup ---
@app.on_event("startup")
def startup_event():
  db = SessionLocal()
  try:
      seed_data(db)
  finally:
      db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

# Register pet routes
app.include_router(pets_router)
app.include_router(appointments_router)
