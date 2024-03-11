import os
from os import environ as env
import sys
import pytest
from unittest.mock import patch
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.auth_service import AuthService
from entity.user import User

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_generate_jwt_token():
    auth_service = AuthService()
    
    token = auth_service.generate_jwt_token("test_user_id")
    assert token is not None

def test_login_service_success():
    auth_service = AuthService()

    user = User(
        "tanmeshnm@gmail.com",
        "admin",
        "calendly_token",
        "calendly_user_url",
    )

    with patch.dict('services.auth_service.db', {"tanmeshnm@gmail.com": user}):
        result, token = auth_service.login_service("tanmeshnm@gmail.com", "admin")
    
        assert result == "success"
        assert token is not None

def test_login_service_invalid_credentials():
    auth_service = AuthService()

    user = User(
        "tanmeshnm@gmail.com",
        "admin2",
        "calendly_token",
        "calendly_user_url",
    )

    with patch.dict('services.auth_service.db', {"tanmeshnm@gmail.com": user}):
        result, message = auth_service.login_service("invalid_email@gmail.com", "invalid_password")
        
        assert result == "error"
        assert message == "Invalid email or password!"

def test_signup_service_success():
    auth_service = AuthService()

    result, message = auth_service.signup_service("new_user@gmail.com", "password123", "calendly_token")
    
    assert result == "success"
    assert message == "User registered successfully!"

if __name__ == "__main__":
    pytest.main()
