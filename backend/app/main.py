from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.pet_routes import router as pets_router

app = FastAPI(title="Pet Sitting API")

# CORS so frontend can talk to backend
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


@app.get("/health")
def health():
    return {"status": "ok"}


# Register pet routes
app.include_router(pets_router)
