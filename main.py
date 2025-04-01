from fastapi import FastAPI, status, Depends, HTTPException
from app.database.models import Base
from sqlalchemy.orm import Session
from app.database.db import SessionLocal, engine
from app.api_router.user_router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='GPT4')
app.include_router(router)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_config():
    return Settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)