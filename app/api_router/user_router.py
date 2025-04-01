from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.schemas import UserCreate, LoginUser, ChangePassword, UserOut, UserUpdate
from passlib.context import CryptContext
from authx import AuthX
from app.database.db import get_db
from app.config import settings
from datetime import timedelta


secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM


router = APIRouter()
class AuthXConfig:
    JWT_SECRET_KEY = secret_key
    JWT_ALGORITHM = algorithm
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_COOKIE_NAME = "csrf_access_token"
    JWT_COOKIE_SAME_SITE = "Strict"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ENCODE_AUDIENCE = None
    JWT_ENCODE_ISSUER = None
    private_key = secret_key 


    @classmethod
    def has_location(cls, location: str) -> bool:
        return location in cls.JWT_TOKEN_LOCATION


security = AuthX(config=AuthXConfig())


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
  
  
def hashed_password(password):
    return pwd_context.hash(password)      
        
        
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


@router.post("/user/", response_model=UserOut, status_code=201)
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
        password=hashed_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)


def get_userdb(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_userdb(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    update_data: UserUpdate = Body(...),
    db: Session = Depends(get_db)
):
    db_user = get_userdb(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.username:
        db_user.username = update_data.username
    if update_data.email:
        db_user.email = update_data.email
    if update_data.password:
        db_user.password = hashed_password(update_data.password)

    db.commit()
    db.refresh(db_user)
    return UserOut.model_validate(db_user)


@router.delete("/users/{user_id}", response_model=UserCreate)
def remove_user(user_id:int, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


