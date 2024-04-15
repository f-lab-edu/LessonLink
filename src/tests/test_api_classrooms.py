from functions.init_file import get_init_config_data, set_init_config_data
from tests.test_login import test_post_instructor_login_handler, test_post_student_login_handler, test_post_student_login_handler_admin


def test_get_classroom_handler(client, student_credentials, instructor_credentials, login):
    access_token = test_post_student_login_handler(
        student_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/classrooms", headers=headers)
    assert response.status_code == 200

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/classrooms", headers=headers)
    assert response.status_code == 200


def test_post_create_classroom_handler(client, admin_credentials, student_credentials, instructor_credentials, login):
    access_token = test_post_student_login_handler(
        student_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "name": "test",
        "capacity": 10,
        "location": "test",
        "building_name": "test"
    }

    response = client.post("/classrooms", headers=headers, json=request_body)
    assert response.status_code == 401

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post("/classrooms", headers=headers, json=request_body)
    assert response.status_code == 401

    access_token = test_post_student_login_handler_admin(
        admin_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post("/classrooms", headers=headers, json=request_body)
    set_init_config_data("classrooms", "id", str(response.json()["id"]))

    assert response.status_code == 201


def test_get_classroom_by_id_handler(client, student_credentials, instructor_credentials, login):

    classroom_id = get_init_config_data("classrooms", "id")

    access_token = test_post_student_login_handler(
        student_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 200

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 200


def test_patch_classroom_handler(client, admin_credentials, student_credentials, instructor_credentials, login):

    classroom_id = get_init_config_data("classrooms", "id")

    access_token = test_post_student_login_handler(
        student_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "name": "test1",
        "capacity": 100,
        "location": "test1",
        "building_name": "test1"
    }

    response = client.patch(
        f"/classrooms/{classroom_id}", headers=headers, json=request_body)
    assert response.status_code == 401

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch(
        f"/classrooms/{classroom_id}", headers=headers, json=request_body)
    assert response.status_code == 401

    access_token = test_post_student_login_handler_admin(
        admin_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch(
        f"/classrooms/{classroom_id}", headers=headers, json=request_body)
    assert response.status_code == 200


def test_delete_classroom_handler(client, admin_credentials, student_credentials, instructor_credentials, login):
    classroom_id = get_init_config_data("classrooms", "id")

    access_token = test_post_student_login_handler(
        student_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(
        f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 401

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(
        f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 401

    access_token = test_post_student_login_handler_admin(
        admin_credentials, login
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(
        f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/classrooms/{classroom_id}", headers=headers)
    assert response.status_code == 404
