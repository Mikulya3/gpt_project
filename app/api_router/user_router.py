from app.models import User
from app.schemas import UserBase,  LoginUser
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from datetime import timedelta, datetime
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.crud.crud_user import create_user, get_user, delete_user
from app.config import settings
from datetime import date, datetime, timedelta, time
from app.auth import create_access_token, create_refresh_token
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
router = APIRouter() 
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
outh2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

        
@router.post("/login")
def login_user(user=LoginUser, db: Session = Depends(get_db)):
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    
    user = get_user(db, user.email)
    token =  create_access_token(user.id, timedelta(minutes=30)) 
    refresh = create_refresh_token(user.id,timedelta(minutes = 1008))

    return {'access_token': token, 'token_type': 'bearer','refresh_token':refresh,"user_id":user.id}



@router.post("/user/", response_model=UserBase, status_code=201)
def register_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)).first()
    if db_user:
        if db_user.username==user.username:
            raise HTTPException(status_code=400, detail="User already with this username registered")
    if db_user:
        if db_user.email==user.email:
            raise HTTPException(status_code=400, detail="User already with this email registered")
        
        
    new_user = create_user(db, user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/", response_model=list[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

    
@router.put("/users/{user_id}", response_model=UserBase)
def update_user(user_id:int, db:Session=Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=UserBase)
def remove_user(user_id:int, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
    