from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pet Sitting API (Skeleton)")

# CORS – allow frontend to talk to backend in dev
origins = [
    "http://localhost:9000",  # Quasar dev default
    "http://localhost:5173",  # Vite default, just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
