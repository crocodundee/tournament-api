def test_registration(client):
    response = client.post(
        '/users/sign-up',
        json={
            'email': 'test@email.com',
            'password1': 'defaultpass',
            'password2': 'defaultpass'
        }
    )
    assert response.status_code == 201, response.json()
