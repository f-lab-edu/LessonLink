from functions.init_file import get_init_config_data
from tests.test_login import test_post_instructor_login_handler
import secrets

def test_post_create_course_handler_large_data(
    client, credentials, login_get_access_token
):
    id = get_init_config_data('test_account', 'instructor_ID')

    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    for i in range(1000000, 1001000):
        request_body = {
            "id": i,
            "name": secrets.token_urlsafe(8),
            "description": secrets.token_urlsafe(8),
            "start_date": "2024-04-11",
            "end_date": "2024-04-11",
            "instructor_id": id,
            "cost": 500000
        }

        response = client.post("/courses", headers=headers, json=request_body)
        assert response.status_code == 201

def test_patch_course_handler_instructor_large_data(
    client, credentials, login_get_access_token
):

    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    for i in range(1000000, 1001000):

        id = get_init_config_data('test_account', 'instructor2_ID')
        request_body = {
            "id": i,
            "name": secrets.token_urlsafe(8),
            "description": secrets.token_urlsafe(8),
            "start_date": "2024-04-10",
            "end_date": "2024-04-10",
            "instructor_id": id,
            "cost": 200000
        }

        response = client.patch(f"/courses/{i}",
                                headers=headers, json=request_body)
        assert response.status_code == 200


def test_delete_course_handler_instructor_large_data(
    client, credentials, login_get_access_token
):
        # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    for i in range(1000000, 1001000):

        response = client.delete(f"/courses/{i}", headers=headers)
        assert response.status_code == 204