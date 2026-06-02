import pytest
from fastapi.testclient import TestClient
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# create a fixture with a context manager to handle startup/lifespan events
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# generate a random email for this test session to avoid conflicts with existing users
test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
test_password = "securepassword123"

def test_register_user(client):
    """Verify that a new user can register and receive a token."""
    response = client.post(
        "/auth/register",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code == 201

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_user(client):
    """Verify that registering with an existing email fails."""
    response = client.post(
        "/auth/register",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_login_success(client):
    """Verify that the user can log in with correct credentials."""
    # login uses OAuth2 password flow, so we send form data
    response = client.post(
        "/auth/login",
        data={"username": test_email, "password": test_password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client):
    """Verify that login fails with incorrect credentials."""
    response = client.post(
        "/auth/login",
        data={"username": test_email, "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid email or password"