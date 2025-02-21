def test_registration(client):
    response = client.post(
        "/api/sign-up/", json={"email": "test@email.com", "password": "defaultpass"}
    )
    assert response.status_code == 201
