def test_registration(client):
    response = client.post(
        "/users/sign-up",
        json={"email": "test@email.com", "password": "defaultpass"}
    )
    assert response.status_code == 201
