from django.urls import reverse

from apps.bnpl.factories import PaymentPlanFactory


def test_get_plans(merchant_user_api_client, merchant_user):
    PaymentPlanFactory.create_batch(5)
    PaymentPlanFactory.create_batch(5, merchant=merchant_user)
    url = reverse("plans_api")
    response = merchant_user_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


def test_get_plans_as_user(user_api_client, user):
    PaymentPlanFactory.create_batch(5)
    PaymentPlanFactory.create_batch(5, user=user)
    url = reverse("plans_api")
    response = user_api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


def test_create_plan_as_merchant(merchant_user_api_client, merchant_user, user):
    url = reverse("plans_api")
    data = {
        "user_email": "user@bnpl.co",
        "total_amount": "100",
        "start_date": "2025-04-30",
        "number_of_installments": 4,
    }
    response = merchant_user_api_client.post(url, data)
    assert response.status_code == 200


def test_create_plan_as_user(user_api_client, user):
    url = reverse("plans_api")
    data = {
        "user_email": "user@bnpl.co",
        "total_amount": "100",
        "start_date": "2025-04-30",
        "number_of_installments": 4,
    }
    response = user_api_client.post(url, data)
    assert response.status_code == 403
