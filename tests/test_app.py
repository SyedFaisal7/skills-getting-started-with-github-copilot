from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_expected_data():
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity_name in data
    assert "description" in data[expected_activity_name]
    assert "participants" in data[expected_activity_name]


def test_signup_participant_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Verify participant was added
    details = client.get("/activities").json()[activity_name]
    assert email in details["participants"]


def test_signup_duplicate_participant_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_participant_removes_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "remove-me@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    # Verify participant was removed
    details = client.get("/activities").json()[activity_name]
    assert email not in details["participants"]
