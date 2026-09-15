def test_valid_login_returns_customer_profile(api_client, credentials):
    response = api_client.login(credentials["username"], credentials["password"])

    assert response.status_code == 200
    body = response.json()
    assert body["id"] > 0
    assert "firstName" in body
    assert "lastName" in body


def test_invalid_login_is_rejected(api_client):
    response = api_client.login("not_a_real_user", "wrong-password")

    assert response.status_code == 400
