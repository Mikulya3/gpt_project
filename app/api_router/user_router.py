from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.schemas import UserCreate, LoginUser, ForgotPassword, ResetPassword, UserOut, UserUpdate
from passlib.context import CryptContext
from authx import AuthX, TokenPayload, AuthXConfig
from app.database.db import get_db
from app.config import settings, mail_config
from datetime import timedelta, datetime
import datetime 
from fastapi_mail import FastMail, MessageSchema

security_scheme = HTTPBearer()
user_router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY: str = settings.SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME: str = "access_token"


security = AuthX(config=config)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
  
  
def hashed_password(password):
    return pwd_context.hash(password)      
        
        
@user_router.post("/login")
def login_user(login_data: LoginUser, response: Response, db: Session = Depends(get_db)
):
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

    security._set_cookies(response=response, type="access", token=token)

    return {"access_token": token, "token_type": "bearer"}


@user_router.post("/user/", response_model=UserOut, status_code=201)
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

@user_router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_userdb(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user)


@user_router.put("/users/{user_id}", response_model=UserOut)
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
    if update_data.is_staff is not None:
        db_user.is_staff = update_data.is_staff

    db.commit()
    db.refresh(db_user)
    return UserOut.model_validate(db_user)


@user_router.delete("/users/{user_id}", response_model=UserCreate)
def remove_user(user_id: int, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


def create_reset_token(email: str):
    expire_time = datetime.datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(
        {"sub": email, "exp": expire_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_reset_token(token: str):
    try:
        payload =  jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token") 


@user_router.post("/forgot_password")
async def forget_password(request: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404,  detail="User not found")
    token = create_reset_token(user.email)
    reset_link = f"http://127.0.0.1:8000/reset_password?token={token}"
    message = MessageSchema(
        subject="reset password", 
        recipients=[user.email],
        body=f"""
        <p>Greetings!</p>
        <p>to reset password, please click on the button:</p>
        <a href="{reset_link}" style="
            display: inline-block;
            padding: 12px 24px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;">
            Сбросить пароль
        </a>
        <p>If you did not request a password reset, ignore this letter.</p>
    """,
    subtype="html"
)
    fm = FastMail(mail_config)
    await fm.send_message(message)
    
    return {"message": "Password reset link sent to your email."}


@user_router.post("/reset_password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    email = decode_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400,  detail="invalid token or expired")
    
    user = db.query(User).filter(User.email == email).first()   
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    user.password = hashed_password(data.new_password)
    db.commit()
    return {"message": "Password reset successfully"}


@user_router.get("/reset_password")
def check_token(token: str):
    email = decode_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Token invalid or expired")
    return {"message": "Token valid"}















def check_admin(
    db: Session = Depends(get_db),
    token_payload: TokenPayload = Depends(security.access_token_required)
):
    email = token_payload.sub
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


@user_router.get("/admin/users/", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), _: User = Depends(check_admin), __: HTTPAuthorizationCredentials = Depends(security_scheme)):
    return db.query(User).all()


def get_current_user(token_payload=Depends(security.access_token_required)):
    return token_payload.sub 