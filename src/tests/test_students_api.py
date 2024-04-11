from functions.init_file import get_init_config_data
from tests.conftest import login
from tests.test_login import test_post_student_login_handler, test_post_student_login_handler_admin


def test_get_students_handler(client, admin_credentials, login):

    id, pw = admin_credentials

    access_token = test_post_student_login_handler_admin(
        admin_credentials, login)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/students", headers=headers)
    assert response.status_code == 200


def test_get_student_by_id_handler(client, student_credentials, login):
    access_token = test_post_student_login_handler(
        student_credentials, login)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    id = get_init_config_data('test_account', 'STUDENT_ID')
    response = client.get(f"/students/{id}", headers=headers)
    assert response.status_code == 200

    id2 = get_init_config_data('test_account', 'STUDENT2_ID')
    response = client.get(f"/students/{id2}", headers=headers)
    assert response.status_code == 401

    response = client.get(f"/students/", headers=headers)
    assert response.status_code == 401


def test_post_create_id_handler(client):

    request_body1 = {
        "id": get_init_config_data('test_account', 'STUDENT3_ID'),
        "pw": get_init_config_data('test_account', 'STUDENT3_PW'),
        "name": "string",
        "contact": "string",
        "email": "string@string",
        "birth_date": "2024-04-11",
        "gender": "Male",
        "join_date": "2024-04-11"
    }

    request_body2 = {
        "id": get_init_config_data('test_account', 'STUDENT_ID'),
        "pw": get_init_config_data('test_account', 'STUDENT_PW'),
        "name": "string",
        "contact": "string",
        "email": "string@string",
        "birth_date": "2024-04-11",
        "gender": "Male",
        "join_date": "2024-04-11"
    }

    response = client.post("/students/", json=request_body1)
    assert response.status_code == 201

    response = client.post("/students/", json=request_body2)
    assert response.status_code == 409


def test_post_student3_login_handler(student3_credentials, login):
    id, pw = student3_credentials
    access_token = login("/students/log-in", id, pw)
    return access_token


def test_patch_update_student_pw_by_id_handler(client, student3_credentials, login):

    access_token = test_post_student3_login_handler(
        student3_credentials, login)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "pw": get_init_config_data('test_account', 'STUDENT3_PW_PATCH')
    }

    response = client.patch("/students/testacct_student3", json=request_body)
    assert response.status_code == 401

    response = client.patch("/students/testacct_student3",
                            json=request_body, headers=headers)

    assert response.status_code == 200


def test_post_student3_patched_login_handler(student3_patched_credentials, login):
    id, pw = student3_patched_credentials
    access_token = login("/students/log-in", id, pw)
    return access_token


def test_delete_student_handler(client, student3_patched_credentials, login):

    access_token = test_post_student3_patched_login_handler(
        student3_patched_credentials, login)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(
        "/students/testacct_student3", headers=headers)

    assert response.status_code == 204

    id = get_init_config_data('test_account', 'STUDENT3_ID')
    response = client.get(f"/students/{id}", headers=headers)
    assert response.status_code == 404
