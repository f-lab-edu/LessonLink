from tests.test_login import test_post_student_login_handler


def test_post_student_login_handler_caching(credentials, login_get_access_token):
    for _ in range(100):
        access_token = test_post_student_login_handler(
            credentials, login_get_access_token
        )

