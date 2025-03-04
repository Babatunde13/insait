import pytest
from unittest.mock import patch, MagicMock
from app.services.auth import AuthService
from app.models import User
from app.extensions import db

@pytest.fixture
def mock_create_access_token():
    with patch("app.services.auth.create_access_token", return_value="mock_token") as mock_token:
        yield mock_token

def test_register_user_success(client):
    response = AuthService.register_user("test_user", "securepassword")

    assert response == {"message": "User registered successfully", "data": {}}

def test_register_user_existing(client, test_user):
    response = AuthService.register_user(test_user.username, "securepassword")
    assert response == {"error": "User already exists"}

def test_authenticate_user_success(test_user, mock_create_access_token):
    response = AuthService.authenticate_user(test_user.username, test_user.password)
    assert response == {
        "data": {"access_token": "mock_token"},
        "message": "User authenticated successfully"
    }

    assert mock_create_access_token.call_count == 1

def test_authenticate_user_in_different_case(test_user, mock_create_access_token):
    response = AuthService.authenticate_user(test_user.username.upper(), test_user.password)
    assert response == {
        "data": {"access_token": "mock_token"},
        "message": "User authenticated successfully"
    }

    assert mock_create_access_token.call_count == 1

def test_authenticate_user_invalid(test_user):
    response = AuthService.authenticate_user(test_user.username, "wrong_password")
    assert response == {"error": "Invalid credentials"}

    response = AuthService.authenticate_user("wrong_username", test_user.password)
    assert response == {"error": "Invalid credentials"}
