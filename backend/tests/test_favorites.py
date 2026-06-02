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

# fixture that automatically logs a fresh dummy user in and shares their token with tests
@pytest.fixture(scope="module")
def auth_token(client):
    test_email = f"fav_user_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "securepassword123"

    # register
    client.post(
        "/auth/register",
        json={"email": test_email, "password": test_password}
    )

    # login and grab token
    response = client.post(
        "/auth/login",
        data={"username": test_email, "password": test_password}
    )
    return response.json()["access_token"]


# pick random embedding id in database
TEST_EMBEDDING_ID = 7670

def test_unauthorized_access(client):
    """Verify that requests without an Authorization token are rejected."""
    response = client.get(f"/favorites")
    assert response.status_code == 401

def test_add_favorite(client, auth_token):
    """Verify that a logged-in user can add a fragrance to their favorites."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/favorites/{TEST_EMBEDDING_ID}", headers=headers)

    assert response.status_code == 201
    assert response.json() == {"message": "Fragrance added to favorites"}

def test_get_favorites(client, auth_token):
    """Verify that a logged-in user can retrieve their list of favorite fragrances."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/favorites", headers=headers)

    assert response.status_code == 200
    data = response.json()

    # check that it returns a list and our favorited record is in it
    assert isinstance(data, list)
    assert any(fav["embedding_id"] == TEST_EMBEDDING_ID for fav in data)

def test_remove_favorite(client, auth_token):
    """Verify that a logged-in user can remove a fragrance from their favorites."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/favorites/{TEST_EMBEDDING_ID}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Fragrance removed from favorites"}

    # fetch favorites again to confirm it's gone
    get_response = client.get(f"/favorites", headers=headers)
    assert not any(fav["embedding_id"] == TEST_EMBEDDING_ID for fav in get_response.json())