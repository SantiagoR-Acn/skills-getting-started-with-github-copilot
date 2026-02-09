import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_remove_participant():
    email = "removeme@mergington.edu"
    # Add participant first
    client.post(f"/activities/Gym Class/signup?email={email}")
    # Remove participant
    response = client.delete(f"/activities/Gym Class/participants/{email}")
    assert response.status_code == 200
    # Confirm removal
    participants = client.get("/activities").json()["Gym Class"]["participants"]
    assert email not in participants


def test_remove_nonexistent_participant():
    response = client.delete("/activities/Chess Club/participants/notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/participants/someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
