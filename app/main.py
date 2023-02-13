from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.accounts.router import router as accounts_router
from app.api.transactions.router import router as transactions_router


app = FastAPI(
    title="FastAPI Boilerplate",
    description="A boilerplate for FastAPI",
    version="0.0.1",
    docs_url="/",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

