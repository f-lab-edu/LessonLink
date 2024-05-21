from functions.init_file import get_init_config_data
from tests.test_login import test_post_instructor_login_handler, test_post_student_login_handler


def test_post_bucket_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "id": get_init_config_data('test_account', 'INSTRUCTOR_ID'),
        "course_id": 2147483601
    }

    response = client.post("/bucket", headers=headers, json=request_body)
    assert response.status_code == 401

def test_post_bucket_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "id": get_init_config_data('test_account', 'STUDENT_ID'),
        "course_id": 2147483601
    }

    response = client.post("/bucket", headers=headers, json=request_body)
    assert response.status_code == 201

def test_get_bucket_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )

    id = get_init_config_data('test_account', 'STUDENT_ID')
    id2 = get_init_config_data('test_account', 'STUDENT2_ID')

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/bucket/{id2}", headers=headers)
    assert response.status_code == 401

    response = client.get(f"/bucket/{id}", headers=headers)
    assert response.status_code == 200


def test_delete_bucket_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )

    id = get_init_config_data('test_account', 'STUDENT_ID')

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(f"/bucket/{id}/2147483601", headers=headers)
    assert response.status_code == 204

    response = client.delete(f"/bucket/{id}/2147483601", headers=headers)
    assert response.status_code == 404
