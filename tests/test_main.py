from _pytest.fixtures import fixture
from fastapi.testclient import TestClient
from starlette import status

from src.main import Post, app

client = TestClient(app)


# 모든 테스트 함수가 실행되기 전에 항상 실행되는 함수다.
# 테스트 함수마다 독립된 환경을 만들어주는 로직이 보통 여기에 포함된다.
@fixture(autouse=True, scope="function")
def setup():
    # 서버 내의 Post 데이터를 비워준다.
    app.posts = {}


# `POST /posts/{post_id}` API가 성공적으로 동작한다.
def test_create_post_successfully():
    # when
    # `POST /posts/{post_id}` API를 호출한다.
    response = client.post(
        "/posts",
        json={
            "title": "title",
            "content": "content",
        },
    )

    # then
    # 응답 상태 코드가 201이어야 한다.
    assert response.status_code == status.HTTP_201_CREATED

    # 응답 본문이 예상한 형식과 같아야 한다.
    data = response.json()
    assert data == {
        "id": 0,
        "title": "title",
        "content": "content",
        "created_at": data["created_at"],
    }

    # 서버 내에 Post 데이터가 저장되어 있어야 한다.
    assert app.posts[0] == Post(
        id=0,
        title="title",
        content="content",
        created_at=data["created_at"],
    )


# `GET /posts/{post_id}` API가 성공적으로 동작한다.
def test_get_post_successfully():
    # given
    # 서버 내에 Post 데이터가 저장되어 있다.
    app.posts[0] = Post(
        id=0,
        title="title",
        content="content",
    )

    # when
    # `GET /posts/{post_id}` API를 호출한다.
    response = client.get("/posts/0")

    # then
    # 응답 상태 코드가 200이어야 한다.
    assert response.status_code == status.HTTP_200_OK

    # 응답 본문이 예상한 형식과 같아야 한다.
    data = response.json()
    assert data == {
        "id": 0,
        "title": "title",
        "content": "content",
        "created_at": data["created_at"],
    }


# `GET /posts/{post_id}` API가 존재하지 않는 Post에 대해 404를 응답한다.
def test_get_post_with_non_existing_post_id():
    # given
    # 존재하지 않는 Post ID가 주어졌다.
    post_id = 0

    # when
    # `GET /posts/{post_id}` API를 호출한다.
    response = client.get(f"/posts/{post_id}")

    # then
    # 응답 상태 코드가 404이어야 한다.
    assert response.status_code == status.HTTP_404_NOT_FOUND


# `GET /posts` API가 성공적으로 동작한다.
def test_get_posts_successfully():
    # given
    # 서버 내에 Post 데이터가 저장되어 있다.
    app.posts[0] = Post(
        id=0,
        title="title 1",
        content="content 1",
    )
    app.posts[1] = Post(
        id=1,
        title="title 2",
        content="content 2",
    )

    # when
    # `GET /posts` API를 호출한다.
    response = client.get("/posts")

    # then
    # 응답 상태 코드가 200이어야 한다.
    assert response.status_code == status.HTTP_200_OK

    # 응답 본문이 예상한 형식과 같아야 한다.
    data = response.json()
    assert data == [
        {
            "id": 1,
            "title": "title 2",
            "content": "content 2",
            "created_at": data[1]["created_at"],
        },
        {
            "id": 0,
            "title": "title 1",
            "content": "content 1",
            "created_at": data[0]["created_at"],
        },
    ]
