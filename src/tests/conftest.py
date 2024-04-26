from fastapi.testclient import TestClient
import pytest
from functions.init_file import get_init_config_data
from main import app


@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture
def credentials():
    return {
        'admin': {
            'id': get_init_config_data('admin_account', 'ID'),
            'pw': get_init_config_data('admin_account', 'PW')
        },
        'student': {
            'id': get_init_config_data('test_account', 'STUDENT_ID'),
            'pw': get_init_config_data('test_account', 'STUDENT_PW')
        },
        'student2': {
            'id': get_init_config_data('test_account', 'STUDENT2_ID'),
            'pw': get_init_config_data('test_account', 'STUDENT2_PW')
        },
        'student3': {
            'id': get_init_config_data('test_account', 'STUDENT3_ID'),
            'pw': get_init_config_data('test_account', 'STUDENT3_PW')
        },
        'student3_patched': {
            'id': get_init_config_data('test_account', 'STUDENT3_ID'),
            'pw': get_init_config_data('test_account', 'STUDENT3_PW_PATCH')
        },
        'instructor': {
            'id': get_init_config_data('test_account', 'INSTRUCTOR_ID'),
            'pw': get_init_config_data('test_account', 'INSTRUCTOR_PW')
        },
        'instructor2': {
            'id': get_init_config_data('test_account', 'INSTRUCTOR2_ID'), 
            'pw': get_init_config_data('test_account', 'INSTRUCTOR2_PW')
        },
        'instructor3': {
            'id': get_init_config_data('test_account', 'INSTRUCTOR3_ID'),
            'pw': get_init_config_data('test_account', 'INSTRUCTOR3_PW')
        },
        'instructor3_patched': {
            'id': get_init_config_data('test_account', 'INSTRUCTOR3_ID'),
            'pw':  get_init_config_data('test_account', 'INSTRUCTOR3_PW_PATCH')
        }
    }

@pytest.fixture
def login_get_access_token(client):
    def login_user(endpoint, login_data):
        response = client.post(endpoint, json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        return response.json()["access_token"]
    return login_user