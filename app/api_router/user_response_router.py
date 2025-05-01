from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.models import User_Response, User
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import UserResponseCreate, UserResponseBase
from authx import AuthX, AuthXConfig, RequestToken


response_router = APIRouter()
security = AuthX(config=AuthXConfig())


@response_router.post("/responses/", response_model=UserResponseBase, status_code=status.HTTP_201_CREATED)
def response_user(response: UserResponseCreate, request: Request, token: RequestToken = Depends(security.get_token_from_request(optional=False)), db: Session = Depends(get_db)):
    payload = security.verify_token(token)
    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    ip_address = request.client.host
    user_response = User_Response(
        owner_id=user.id,
        ip_address=ip_address,
        **response.dict()
    )
    db.add(user_response)
    db.commit()
    db.refresh(user_response)
    return UserResponseBase.model_validate(user_response)
    
