from fastapi.testclient import TestClient

from main import app
from functions.init_file import get_init_config_data

client = TestClient(app=app)


def test_post_student_login_handler_admin():
    admin_id = get_init_config_data('admin_account', 'ID')
    admin_pw = get_init_config_data('admin_account', 'PW')

    login_data = {
        "id": admin_id,
        "pw": admin_pw
    }

    response = client.post("/students/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_post_student_login_handler():
    id = get_init_config_data('test_account', 'STUDENT_ID')
    pw = get_init_config_data('test_account', 'STUDENT_PW')

    login_data = {
        "id": id,
        "pw": pw
    }

    response = client.post("/students/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_post_student2_login_handler():
    id = get_init_config_data('test_account', 'STUDENT2_ID')
    pw = get_init_config_data('test_account', 'STUDENT2_PW')

    login_data = {
        "id": id,
        "pw": pw
    }

    response = client.post("/students/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_post_instructor_login_handler():
    id = get_init_config_data('test_account', 'INSTRUCTOR_ID')
    pw = get_init_config_data('test_account', 'INSTRUCTOR_PW')

    login_data = {
        "id": id,
        "pw": pw
    }

    response = client.post("/instructors/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token


def test_post_instructor_login_handler():
    id = get_init_config_data('test_account', 'INSTRUCTOR2_ID')
    pw = get_init_config_data('test_account', 'INSTRUCTOR2_PW')

    login_data = {
        "id": id,
        "pw": pw
    }

    response = client.post("/instructors/log-in", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    return access_token
