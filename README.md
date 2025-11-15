# Pet Sitting App

Full-stack demo app with a **FastAPI** backend and **Vue 3 + Quasar + Pinia** frontend.

## Backend (FastAPI)
### Local setup

```text
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URLs:
- API root: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs

### Docker 

```text
cd backend
docker build -t pet-backend .
docker run --name pet-api -p 8000:8000 pet-backend
```

Stop/Start

`
docker stop pet-api
docker start pet-api
`

## Frontend (Vue 3 + Quasar + Pinia)
### Local setup

```text
cd frontend
npm install
npm run dev
```

Frontend URL:

- http://localhost:5173

The frontend connects to the backend at `http://localhost:8000`.
