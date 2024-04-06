from fastapi.testclient import TestClient

from main import app
from functions.init_file import get_init_config_data
from tests.test_login import test_post_student_login_handler, test_post_student_login_handler_admin

client = TestClient(app=app)


def test_get_students_handler():
    access_token = test_post_student_login_handler_admin()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/students", headers=headers)
    assert response.status_code == 200


def test_get_student_by_id_handler():
    access_token = test_post_student_login_handler()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    print(access_token)

    id = get_init_config_data('test_account', 'STUDENT_ID')
    response = client.get(f"/students/{id}", headers=headers)
    assert response.status_code == 200

    id2 = get_init_config_data('test_account', 'STUDENT2_ID')
    response = client.get(f"/students/{id2}", headers=headers)
    assert response.status_code == 401


def test_post_create_id_handler():
    pass


def test_patch_update_student_pw_by_id_handler():
    pass


def test_delete_student_handler():
    pass
