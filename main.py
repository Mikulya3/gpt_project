from fastapi import FastAPI, status, Depends, HTTPException
from app.database.models import Base
from app.database.db import engine
from fastapi.middleware.cors import CORSMiddleware
from app.api_router.user_router import user_router
from app.api_router.user_response_router import response_router 
from app.api_router.pdf_router import pdf_router

app = FastAPI(title='GPT4')
Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(response_router)
app.include_router(pdf_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)