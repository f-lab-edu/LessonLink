def test_post_student_login_handler_admin(admin_credentials, login):
    id, pw = admin_credentials
    access_token = login("/students/log-in", id, pw)
    return access_token


def test_post_student_login_handler(student_credentials, login):
    id, pw = student_credentials
    access_token = login("/students/log-in", id, pw)
    return access_token


def test_post_student2_login_handler(student2_credentials, login):
    id, pw = student2_credentials
    access_token = login("/students/log-in", id, pw)
    return access_token


def test_post_instructor_login_handler(instructor_credentials, login):
    id, pw = instructor_credentials
    access_token = login("/instructors/log-in", id, pw)
    return access_token


def test_post_instructor_login_handler(instructor2_credentials, login):
    id, pw = instructor2_credentials
    access_token = login("/instructors/log-in", id, pw)
    return access_token
