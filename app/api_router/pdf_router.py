from fastapi import APIRouter, HTTPException, Depends
from app.database.models import User_Response
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import UserResponseBase
from app.services.gpt_prompts import sorting_data, built_promts
import uuid
from app.services.pdf_generator import generate_pdf

pdf_router = APIRouter()


@pdf_router.get("/generate_context", response_model=dict)
def get_context(student_name: str, db: Session = Depends(get_db)):
    context = sorting_data(db, student_name)
    return context


@pdf_router.get("/generate_prompts", response_model=dict)
def generation(context: dict):
    if not context:
        raise HTTPException(status_code=404, detail="No context found for this user")
    
    gpt_outputs = built_promts(context)
    data = {**context, **gpt_outputs}
    filename = f"{data['student_profile']['name'].replace(' ', '_')}_{uuid.uuid4().hex[:6]}.pdf"
    output_path = f"app/generated_reports/{filename}"
    generate_pdf(data, output_path) 
    
    return {
        "pdf_url": output_path,
        **gpt_outputs
    }
    
    
    