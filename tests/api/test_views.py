def test_healthcheck(client):
    response = client.get("/")
    assert response.json() == {"status": "ok"}
