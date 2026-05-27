from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_signup_for_activity_adds_participant():
    original = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = ["existing@example.edu"]

    try:
        response = client.post("/activities/Chess Club/signup?email=newstudent@example.edu")

        assert response.status_code == 200
        assert "newstudent@example.edu" in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Signed up newstudent@example.edu for Chess Club"
    finally:
        activities["Chess Club"]["participants"] = original


def test_signup_rejects_duplicate_participant():
    original = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = ["existing@example.edu"]

    try:
        response = client.post("/activities/Chess Club/signup?email=existing@example.edu")

        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"
    finally:
        activities["Chess Club"]["participants"] = original


def test_unregister_participant_removes_email():
    original = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = ["student@example.edu"]

    try:
        response = client.delete("/activities/Chess Club/signup?email=student@example.edu")

        assert response.status_code == 200
        assert "student@example.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed student@example.edu from Chess Club"
    finally:
        activities["Chess Club"]["participants"] = original
