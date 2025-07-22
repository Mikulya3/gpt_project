from fastapi import APIRouter, HTTPException, Depends, status
from app.database.models import User_Response
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import UserResponseBase
from app.services.gpt_prompts import sorting_data, built_promts
import uuid
from app.services.pdf_generator import generate_pdf
from app.config import settings
from app.database.models import User
from app.api_router.user_router import get_current_user

pdf_router = APIRouter(prefix="/create_pdf", tags=["create_pdf"])



@pdf_router.get("/", response_model=dict)
def generation(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="No responses found for this user")
    user_response = db.query(User_Response).filter(User_Response.owner_id == user.id).order_by(User_Response.id.desc()).first()
    context = sorting_data(user_response)
    if not context:
        raise HTTPException(status_code=404, detail="No context data found for this user")
    
    gpt_outputs = built_promts(context)
    data = {**context, **gpt_outputs}
    filename = f"{data['student_profile']['name'].replace(' ', '_')}_{uuid.uuid4().hex[:6]}.pdf"
    output_path = f"app/generated_reports/{filename}"
    generate_pdf(data, output_path) 
    
    return {
        "pdf_url": output_path,
        **gpt_outputs
    }
    
    
    