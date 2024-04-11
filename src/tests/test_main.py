
def test_root_handler(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}
