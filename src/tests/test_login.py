from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_post_student_login_handler():
    login_data = {
        "id": 'string',
        "pw": 'string'
    }

    response = client.post("/students/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_post_instructor_login_handler():
    login_data = {
        "id": 'string',
        "pw": 'string'
    }

    response = client.post("/instructors/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token
