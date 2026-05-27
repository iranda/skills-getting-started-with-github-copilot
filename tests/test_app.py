from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email():
    original = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"].append("student@example.edu")

    try:
        response = client.delete("/activities/Chess Club/signup?email=student@example.edu")

        assert response.status_code == 200
        assert "student@example.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed student@example.edu from Chess Club"
    finally:
        activities["Chess Club"]["participants"] = original
