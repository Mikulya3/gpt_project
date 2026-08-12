from app.database.models import User
from app.api_router.user_router import hashed_password
import logging
from unittest.mock import patch, MagicMock
from app.api_router.user_router import get_current_user
from main import app
from app.tasks.email import send_reset_email


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
    user = User(
        username="u",
        email="test@test.com",
        password="x",
    )
    db.add(user)
    db.commit()

    def fake_delay(*args, **kwargs):
        return None

    monkeypatch.setattr(
        send_reset_email,
        "delay",
        fake_delay,
    )

    response = client.post(
        "/forgot_password",
        json={"email": "test@test.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Password reset link sent to your email."
    }




@patch("app.api_router.pdf_router.generate_pdf_task")
@patch(
    "app.api_router.pdf_router.built_prompts",
    return_value={"summary": "test summary"},
)
@patch(
    "app.api_router.pdf_router.sorting_data",
    return_value={"student_profile": {"name": "testuser"}},
)
def test_generate_pdf(mock_sort, mock_build, mock_task, client, db):
    app.dependency_overrides[get_current_user] = (
        lambda: "test@example.com"
    )

    db.add(
        User(
            email="test@example.com",
            username="u",
            password="x",
        )
    )
    db.commit()

    # Fake result returned by generate_pdf_task.delay()
    mock_task.delay.return_value.id = "test-task-id"

    response = client.get("/create_pdf/")

    assert response.status_code == 200
    assert response.json() == {
        "task_id": "test-task-id",
        "status": "PDF generation in progress",
    }

    mock_task.delay.assert_called_once()

    app.dependency_overrides.clear()