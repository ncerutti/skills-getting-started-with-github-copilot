from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_success():
    # Arrange
    activity = "Chess Club"
    test_email = "test@mergington.edu"
    url = f"/activities/{activity.replace(' ', '%20')}/signup?email={test_email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {test_email} for {activity}"

    response = client.get("/activities")
    data = response.json()
    assert test_email in data[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    activity = "Programming Class"
    duplicate_email = "duplicate@mergington.edu"
    signup_url = f"/activities/{activity.replace(' ', '%20')}/signup?email={duplicate_email}"
    client.post(signup_url)

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    # Arrange
    invalid_activity = "Invalid Activity"
    test_email = "test@mergington.edu"
    url = f"/activities/{invalid_activity.replace(' ', '%20')}/signup?email={test_email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_success():
    # Arrange
    activity = "Gym Class"
    delete_email = "delete@mergington.edu"
    signup_url = f"/activities/{activity.replace(' ', '%20')}/signup?email={delete_email}"
    delete_url = f"/activities/{activity.replace(' ', '%20')}/signup?email={delete_email}"
    client.post(signup_url)

    # Act
    response = client.delete(delete_url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {delete_email} from {activity}"

    response = client.get("/activities")
    data = response.json()
    assert delete_email not in data[activity]["participants"]


def test_delete_not_signed_up():
    # Arrange
    activity = "Soccer Team"
    test_email = "notsigned@mergington.edu"
    url = f"/activities/{activity.replace(' ', '%20')}/signup?email={test_email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 400
    assert "Student not signed up" in response.json()["detail"]


def test_delete_invalid_activity():
    # Arrange
    invalid_activity = "Invalid Activity"
    test_email = "test@mergington.edu"
    url = f"/activities/{invalid_activity.replace(' ', '%20')}/signup?email={test_email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
