from rest_framework.reverse import reverse


def test_login_as_merchant_with_correct_cred(merchant_user, api_client):
    data = {
        "email": merchant_user.email,
        "password": "secret_pwd",
    }
    url = reverse("merchant_login_api")
    response = api_client.post(url, data)
    assert response.status_code == 200


def test_login_as_merchant_with_incorrect_cred(merchant_user, api_client):
    data = {
        "email": merchant_user.email,
        "password": "wrong_pwd",
    }
    url = reverse("merchant_login_api")
    response = api_client.post(url, data)
    assert response.status_code == 401


def test_login_as_merchant_to_user_login(merchant_user, api_client):
    data = {
        "email": merchant_user.email,
        "password": "secret_pwd",
    }
    url = reverse("user_login_api")
    response = api_client.post(url, data)
    assert response.status_code == 403


def test_login_as_user_with_correct_cred(user, api_client):
    data = {
        "email": user.email,
        "password": "secret_pwd",
    }
    url = reverse("user_login_api")
    response = api_client.post(url, data)
    assert response.status_code == 200
