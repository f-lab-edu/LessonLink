from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_root_handler():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}
