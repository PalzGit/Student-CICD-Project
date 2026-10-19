
from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Version 1.0" in response.data

def test_student():
    client = app.test_client()
    response = client.get("/student")

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Student"
    assert data["version"] == "1.0"
