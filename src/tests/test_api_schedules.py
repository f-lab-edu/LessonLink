from functions.init_file import get_init_config_data, set_init_config_data
from tests.test_login import test_post_instructor_login_handler, test_post_student_login_handler


def test_get_schedules_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/schedules", headers=headers)
    assert response.status_code == 200


def test_get_schedules_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/schedules", headers=headers)
    assert response.status_code == 200

def test_post_create_schedule_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "course_id": 2147483600,
        "classroom_id": 1,
        "start_time": "00:00:00",
        "end_time": "00:01:00",
        "course_date": "2024-04-10"
    }

    response = client.post("/schedules", headers=headers, json=request_body)
    assert response.status_code == 401


def test_post_create_schedule_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    request_body = {
        "course_id": 2147483600,
        "classroom_id": 1,
        "start_time": "00:00:00",
        "end_time": "00:01:00",
        "course_date": "2024-04-10"
    }

    response = client.post("/schedules", headers=headers, json=request_body)
    set_init_config_data("schedules", "id", str(response.json()["id"]))

    assert response.status_code == 201


def test_get_schedule_by_id_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.get(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 200

    

def test_get_schedule_by_id_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.get(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 200


def test_patch_update_schedule_by_id_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")
    request_body = {
        "course_id": 2147483601,
        "classroom_id": 2,
        "start_time": "00:03:00",
        "end_time": "00:04:00",
        "course_date": "2024-04-11"
    }

    response = client.patch(
        f"/schedules/{schedule_id}", headers=headers, json=request_body)
    assert response.status_code == 401


def test_patch_update_schedule_by_id_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")
    request_body = {
        "course_id": 2147483601,
        "classroom_id": 2,
        "start_time": "00:03:00",
        "end_time": "00:04:00",
        "course_date": "2024-04-11"
    }

    response = client.patch(
        f"/schedules/{schedule_id}", headers=headers, json=request_body)
    assert response.status_code == 200


def test_delete_schedule_handler_student(
    client, credentials, login_get_access_token
):
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.delete(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 401


def test_delete_schedule_handler_instructor(
    client, credentials, login_get_access_token
):
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.delete(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 404
