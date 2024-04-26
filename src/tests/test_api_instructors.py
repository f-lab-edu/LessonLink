from functions.init_file import get_init_config_data
from tests.test_login import test_post_admin_login_handler, test_post_instructor_login_handler, test_post_student_login_handler


def test_get_instructor_handler_student(
    client, credentials, login_get_access_token
):
    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/instructors", headers=headers)
    assert response.status_code == 401


def test_get_instructor_handler_instructor(
    client, credentials, login_get_access_token
):
    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/instructors", headers=headers)
    assert response.status_code == 401


def test_get_instructor_handler_admin(
    client, credentials, login_get_access_token
):
    # 관리자 권한
    access_token = test_post_admin_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/instructors", headers=headers)
    assert response.status_code == 200


def test_get_instructor_by_id_handler(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    id = get_init_config_data('test_account', 'instructor_ID')
    response = client.get(f"/instructors/{id}", headers=headers)
    assert response.status_code == 200

    id2 = get_init_config_data('test_account', 'instructor2_ID')
    response = client.get(f"/instructors/{id2}", headers=headers)
    assert response.status_code == 401

    response = client.get(f"/instructors/", headers=headers)
    assert response.status_code == 401


def test_post_create_instructor_handler(client):

    request_body1 = {
        "id": get_init_config_data('test_account', 'instructor3_ID'),
        "pw": get_init_config_data('test_account', 'instructor3_PW'),
        "name": "string",
        "contact": "string",
        "email": "string"
    }

    request_body2 = {
        "id": get_init_config_data('test_account', 'instructor_ID'),
        "pw": get_init_config_data('test_account', 'instructor_PW'),
        "name": "string",
        "contact": "string",
        "email": "string"
    }

    response = client.post("/instructors/", json=request_body1)
    assert response.status_code == 201

    response = client.post("/instructors/", json=request_body2)
    assert response.status_code == 409


def test_post_instructor3_login_handler(
    credentials, login_get_access_token
):
    return login_get_access_token(
        '/log-in/instructors', credentials['instructor3']
    )


def test_patch_update_instructor_pw_by_id_handler(
    client, credentials, login_get_access_token
):

    access_token = test_post_instructor3_login_handler(
        credentials, login_get_access_token
        )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "pw": get_init_config_data('test_account', 'instructor3_PW_PATCH')
    }

    response = client.patch(
        "/instructors/testacct_instructor3", json=request_body)
    assert response.status_code == 401

    response = client.patch("/instructors/testacct_instructor3",
        json=request_body, headers=headers
    )

    assert response.status_code == 200


def test_post_instructor3_patched_login_handler(
    credentials, login_get_access_token
):
    return login_get_access_token(
        '/log-in/instructors', credentials['instructor3_patched']
    )


def test_delete_instructor_handler(
    client, credentials, login_get_access_token
):

    access_token = test_post_instructor3_patched_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    id = get_init_config_data('test_account', 'instructor3_ID')

    response = client.delete(
        f"/instructors/{id}", headers=headers)

    assert response.status_code == 204

    response = client.get(f"/instructors/{id}", headers=headers)
    assert response.status_code == 404
