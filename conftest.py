import pytest, os
from unittest.mock import patch

from app import create_app
from app.extensions import db
from app.models import User

password = "Password@13"

@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(client):
    """Create a test user."""
    user = User(username="testuser")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    user.password = password
    return user

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for testing protected endpoints."""
    res = client.post("/login", json={"username": test_user.username, "password": test_user.password})
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_openai_create(client):
    with patch("app.services.ai.ai_service.chat_completions.create") as mock:
        mock.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response."
                    }
                }
            ]
        }
        yield mock
