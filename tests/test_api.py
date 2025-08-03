from app.database.models import User
from app.api_router.user_router import hashed_password
import logging
from unittest.mock import patch, MagicMock
from app.api_router.user_router import get_current_user
from main import app


def test_login(client, db):
    # seed user
    email = "test@example.com"
    password = "testpassword"
    hash_password = hashed_password(password)
    
    user = User(email = email, password = hash_password)
    db.add(user)
    db.commit()
    
    payload = {
        "email": email, 
        "password": password
    }
    response = client.post("/login", json=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    


def test_forgot_password_send_email(client, db, monkeypatch):
    user = User(username = "testuser", email="test@test.com", password = "password123")
    db.add(user)
    db.commit()
    db.refresh(user)
    



async def fake_send_message(self, message): pass
def test_forgot_password_send_email(client, db, monkeypatch):
    # 1. seed user
    user = User(username="u", email="test@test.com", password="x")
    db.add(user)
    db.commit()

    # 2. patch FastMail.send_message in the *same* module the route uses
    monkeypatch.setattr(
        "app.api_router.user_router.FastMail.send_message",  
        fake_send_message,
        raising=True,
    )

    # 3. call the route
    resp = client.post("/forgot_password", json={"email": "test@test.com"})
    
    logging.warning("Response JSON: %s", resp.json())
    # 4. assert
    assert resp.status_code == 200
    assert resp.json() == {"message": "Password reset link sent to your email."}
    

@patch("app.api_router.pdf_router.generate_pdf")                       
@patch("app.api_router.pdf_router.built_prompts", return_value={"summary": "test summary"})                       
@patch("app.api_router.pdf_router.sorting_data", return_value={"student_profile": {"name": "testuser"}})         
def test_generate_pdf(mock_sort, mock_build, mock_pdf, client, db):

    # turn off the real authentification
    app.dependency_overrides[get_current_user] = lambda: "test@example.com"

    # seed user
    db.add(User(email="test@example.com", username="u", password="x"))
    db.commit()

    res = client.get("/create_pdf/")          
    assert res.status_code == 200
    assert "pdf_url" in res.json()
    mock_pdf.assert_called_once()
    # clean up
    app.dependency_overrides.clear()