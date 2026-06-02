import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# create a fixture with a context manager to handle startup/lifespan events
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Verify the API is up and running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Noteworthy Fragrances API is running."}

def test_search_pagination_default(client):
    """Verify the endpoint returns the correct default pagination structure."""
    response = client.get("/search/smell?query=white flowers&engine=sbert")
    assert response.status_code == 200
    data = response.json()

    # check pagination metadata
    assert "results" in data
    assert "total_results" in data
    assert "total_pages" in data
    assert "current_page" in data

    # verify default values
    assert data["current_page"] == 1
    assert len(data["results"]) <= 12  # default page size is 12

def test_search_pagination_custom(client):
    """Verify that custom page sizes and page numbers work."""
    response = client.get("/search/smell?query=sweet vanilla&engine=sbert&page=2&page_size=5")
    assert response.status_code == 200

    data = response.json()

    # check that custom pagination parameters are respected
    assert data["current_page"] == 2
    assert len(data["results"]) <= 5  # custom page size of 5


def test_search_validation_error(client):
    """Verify that short queries are rejected."""
    response = client.get("/search/smell?query=hi&engine=sbert")
    assert response.status_code == 422