def test_post_admin_login_handler(credentials, login_get_access_token):
    return login_get_access_token('/log-in/students', credentials['admin'])


def test_post_student_login_handler(credentials, login_get_access_token):
    return login_get_access_token('/log-in/students', credentials['student'])


def test_post_student2_login_handler(credentials, login_get_access_token):
    return login_get_access_token('/log-in/students', credentials['student2'])


def test_post_instructor_login_handler(credentials, login_get_access_token):
    return login_get_access_token('/log-in/instructors', credentials['instructor'])


def test_post_instructor2_login_handler(credentials, login_get_access_token):
    return login_get_access_token('/log-in/instructors', credentials['instructor2'])
