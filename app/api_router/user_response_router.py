from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database.models import User_Response, User
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import UserResponseCreate, UserResponseBase
from authx import AuthX, AuthXConfig, RequestToken
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
from pydantic import ValidationError
from app.config import Settings
from app.api_router.user_router import config 


response_router = APIRouter(prefix="/responses", tags=["responses"], dependencies=[Depends(HTTPBearer())])



security = AuthX(config=config)


@response_router.post("/", response_model=UserResponseBase, status_code=status.HTTP_201_CREATED)
def response_user(response_data: UserResponseCreate, request: Request, token: HTTPAuthorizationCredentials = Security(HTTPBearer()), db: Session = Depends(get_db)):
    request_token = RequestToken(token=token.credentials, location="headers")
    payload = security.verify_token(request_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_email = payload.sub
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    ip_address = request.client.host
    try:
        user_response = User_Response(
            owner_id=user.id,
            ip_address=ip_address,
            **response_data.dict()
        )
    except ValidationError as e:
        print(e.json())
        raise HTTPException(status_code=422, detail=e.errors())
    db.add(user_response)
    db.commit()
    db.refresh(user_response)
    return UserResponseBase.model_validate(user_response)
    
