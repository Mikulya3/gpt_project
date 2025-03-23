from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.schemas import UserCreate, LoginUser, ChangePassword,UserResponse
from passlib.context import CryptContext
from authx import AuthX
from app.database.db import get_db
from app.config import settings
from datetime import timedelta


secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM


router = APIRouter()
config = AuthX()
config.JWT_SECRET_KEY = secret_key
config.JWT_ALGORITHM = algorithm
config.JWT_TOKEN_LOCATION = ["cookies", "headers"]
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_CSRF_COOKIE_NAME = "csrf_access_token"
config.JWT_COOKIE_SAME_SITE = "Strict"
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
security = AuthX(config=config)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
        
        
@router.post("/login")
def login_user(login_data: LoginUser, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or email"
        )
    token = security.create_access_token(uid=user.email)
    response.set_cookie(
        key="csrf_access_token",
        value=token,
        httponly=True,
        secure=settings.ENV == "production",
        samesite="Strict"
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/user/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)).first()
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="User already with this username registered")
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(status_code=400, detail="User already with this email registered")
        
    new_user = User(
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(username=new_user.username, email=new_user.email)

@router.get("/users/", response_model=list[UserCreate])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

    
@router.put("/users/{user_id}", response_model=UserCreate)
def update_user(user_id:int, db:Session=Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", response_model=UserCreate)
def remove_user(user_id:int, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
    