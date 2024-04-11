from fastapi.testclient import TestClient
import pytest
from functions.init_file import get_init_config_data
from main import app


@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture
def admin_credentials():
    return get_init_config_data('admin_account', 'ID'), get_init_config_data('admin_account', 'PW')


@pytest.fixture
def student_credentials():
    return get_init_config_data('test_account', 'STUDENT_ID'), get_init_config_data('test_account', 'STUDENT_PW')


@pytest.fixture
def student2_credentials():
    return get_init_config_data('test_account', 'STUDENT2_ID'), get_init_config_data('test_account', 'STUDENT2_PW')


@pytest.fixture
def student3_credentials():
    return get_init_config_data('test_account', 'STUDENT3_ID'), get_init_config_data('test_account', 'STUDENT3_PW')


@pytest.fixture
def student3_patched_credentials():
    return get_init_config_data('test_account', 'STUDENT3_ID'), get_init_config_data('test_account', 'STUDENT3_PW_PATCH')


@pytest.fixture
def instructor_credentials():
    return get_init_config_data('test_account', 'INSTRUCTOR_ID'), get_init_config_data('test_account', 'INSTRUCTOR_PW')


@pytest.fixture
def instructor2_credentials():
    return get_init_config_data('test_account', 'INSTRUCTOR2_ID'), get_init_config_data('test_account', 'INSTRUCTOR2_PW')


@pytest.fixture
def instructor3_credentials():
    return get_init_config_data('test_account', 'INSTRUCTOR3_ID'), get_init_config_data('test_account', 'INSTRUCTOR3_PW')


@pytest.fixture
def instructor3_patched_credentials():
    return get_init_config_data('test_account', 'INSTRUCTOR3_ID'), get_init_config_data('test_account', 'INSTRUCTOR3_PW_PATCH')


@pytest.fixture
def login(client):
    def login_user(endpoint, id, pw):
        login_data = {
            "id": id,
            "pw": pw
        }
        response = client.post(endpoint, json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        return response.json()["access_token"]
    return login_user
