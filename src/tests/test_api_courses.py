from functions.init_file import get_init_config_data
from tests.test_login import test_post_instructor_login_handler, test_post_student_login_handler


def test_get_courses_handler_student(
    client, credentials, login_get_access_token
):
    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/courses", headers=headers)
    assert response.status_code == 200



def test_get_courses_handler_instructor(
    client, credentials, login_get_access_token
):
    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/courses", headers=headers)
    assert response.status_code == 200


def test_post_create_course_handler_student(
    client, credentials, login_get_access_token
):
    id = get_init_config_data('test_account', 'instructor_ID')

    request_body = {
        "id": 2147483647,
        "name": "string",
        "description": "string",
        "start_date": "2024-04-11",
        "end_date": "2024-04-11",
        "instructor_id": id,
        "cost": 500000
    }

    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post("/courses", headers=headers, json=request_body)
    assert response.status_code == 401


def test_post_create_course_handler_instructor(
    client, credentials, login_get_access_token
):
    
    id = get_init_config_data('test_account', 'instructor_ID')

    request_body = {
        "id": 2147483647,
        "name": "string",
        "description": "string",
        "start_date": "2024-04-11",
        "end_date": "2024-04-11",
        "instructor_id": id,
        "cost": 500000
    }

    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post("/courses", headers=headers, json=request_body)
    assert response.status_code == 201

    response = client.post("/courses", headers=headers, json=request_body)
    assert response.status_code == 409


def test_get_course_by_id_handler_student(
    client, credentials, login_get_access_token
):
    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/courses/2147483647", headers=headers)
    assert response.status_code == 200

    

def test_get_course_by_id_handler_instructor(
    client, credentials, login_get_access_token
):
    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get("/courses/2147483647", headers=headers)
    assert response.status_code == 200


def test_patch_course_handler_student(
    client, credentials, login_get_access_token
):
    id = get_init_config_data('test_account', 'instructor2_ID')

    request_body = {
        "id": 2147483647,
        "name": "string1",
        "description": "string1",
        "start_date": "2024-04-10",
        "end_date": "2024-04-10",
        "instructor_id": id,
        "cost": 200000
    }

    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch("/courses/2147483647",
                            headers=headers, json=request_body)
    assert response.status_code == 401



def test_patch_course_handler_instructor(
    client, credentials, login_get_access_token
):
    
    id = get_init_config_data('test_account', 'instructor2_ID')
    request_body = {
        "id": 2147483647,
        "name": "string1",
        "description": "string1",
        "start_date": "2024-04-10",
        "end_date": "2024-04-10",
        "instructor_id": id,
        "cost": 200000
    }

    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch("/courses/2147483647",
                            headers=headers, json=request_body)
    assert response.status_code == 200

def test_delete_course_handler_student(
    client, credentials, login_get_access_token
):
    # 학생 권한
    access_token = test_post_student_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete("/courses/2147483647", headers=headers)
    assert response.status_code == 401


def test_delete_course_handler_instructor(
    client, credentials, login_get_access_token
):
    # 강사 권한
    access_token = test_post_instructor_login_handler(
        credentials, login_get_access_token
    )
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete("/courses/2147483647", headers=headers)
    assert response.status_code == 204

    response = client.get("/courses/2147483647", headers=headers)
    assert response.status_code == 404