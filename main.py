from fastapi import FastAPI, status, Depends, HTTPException
from app.database.models import Base
from sqlalchemy.orm import Session
from app.database.db import SessionLocal, engine
from app.api_router.user_router import router

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