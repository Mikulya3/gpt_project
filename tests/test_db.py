from app.database.models import User 
from app.api_router.user_router import hashed_password
import logging



def test_register_user_and_get_user(client, db):
    email = "example@example.com"
    user = User(email = email, password = hashed_password("password123"), username="testuser")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    fetched = db.query(User).filter(User.email == email).first()
    assert fetched is not None
    assert fetched.email == email
    assert fetched.username == "testuser"
    

def test_register_duplicate_email_returns_400(client, db):
    db.add(User(username="u", email="dup@example.com", password="x"))
    db.commit()
    
    db.add(User(username="u", email="dup@example.com", password="x"))
    try:
        db.commit()
    except Exception:
        db.rollback()

    payload = {"username": "u2", "email": "dup@example.com", "password": "Pwd1234!"}
    resp = client.post("/user/", json=payload)
    
    logging.warning("Response JSON: %s", resp.json())
    assert resp.status_code == 400
    assert resp.json()["detail"] == "User already with this email registered"
                        

def test_is_staff_false_by_default(client, db):
    user = User(username="eva", email="eva@example.com", password="password123")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.is_staff is False 
    

def test_update_user_email(client, db):
    user = User(username="mik", email="mik@example.com", password="password123")
    db.add(user)
    db.commit()
    db.refresh(user)
    user.email = "testiko@example.com"
    db.commit()
    
    updated_user = db.query(User).filter(User.id == user.id).first()
    assert updated_user.email == "testiko@example.com"
    