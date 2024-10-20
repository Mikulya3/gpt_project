from sqlalchemy.orm import Session
from app.schemas import  UserBase
from app.models import User, Token
from passlib.context import CryptContext
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)



def get_user(db:Session, user_id:int):
    return db.query(User).filter(User.id==user_id).first()


def create_user(db: Session, user: UserBase):
    hashed_password = hash_pass(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session,user:UserBase):
    db_user= db.query(User).filter(User.id==user.id).first()
    if not db_user:
        print("Not found")
    for key,value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user:UserBase):
    db_user=db.query(User).filter(User.id == user.id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user


def get_token(db: Session, token: str):
    return db.query(Token).filter(Token.token == token).first()

def create_token(db: Session, token: str, user_id: int):
    db_token = Token(token=token, user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token