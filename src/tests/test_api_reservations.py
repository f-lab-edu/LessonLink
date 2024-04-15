from functions.init_file import get_init_config_data
from tests.test_login import test_post_student_login_handler, test_post_instructor_login_handler


def test_get_reservations_handler(
    client, student_credentials, instructor_credentials, login
):
    access_token = test_post_student_login_handler(
        student_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/reservations", headers=headers)
    assert response.status_code == 200

    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/reservations", headers=headers)
    assert response.status_code == 200


def test_post_create_reservation_handler_student(
    client, student_credentials, login
):
    access_token = test_post_student_login_handler(
        student_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }


def test_post_create_reservation_handler_instructor(
    client, instructor_credentials, login
):
    pass


def test_get_reservation_by_id_handler(
    client, student_credentials, instructor_credentials, login
):
    pass


def test_patch_update_reservation_by_id_handler(
    client, student_credentials, instructor_credentials, login
):
    pass


def test_delete_reservation_handler(
    client, student_credentials, instructor_credentials, login
):
    pass


def test_delete_schedule_handler_student(
    client, student_credentials, login
):
    access_token = test_post_student_login_handler(
        student_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.delete(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 401


def test_delete_schedule_handler_instructor(
    client, instructor_credentials, login
):
    access_token = test_post_instructor_login_handler(
        instructor_credentials, login
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    schedule_id = get_init_config_data("schedules", "id")

    response = client.delete(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/schedules/{schedule_id}", headers=headers)
    assert response.status_code == 404
