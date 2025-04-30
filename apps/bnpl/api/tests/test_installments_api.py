import pytest
from django.urls import reverse

from apps.bnpl.factories import InstallmentFactory


def test_installment_pay_as_user(user_api_client, user):
    installment = InstallmentFactory.create(payment_plan__user=user)
    url = reverse("installment_pay_api", args=[installment.id])
    response = user_api_client.post(url)
    assert response.status_code == 200


@pytest.mark.main
def test_installment_pay_as_user_to_wrong_installment(user_api_client, user):
    installment = InstallmentFactory.create()
    url = reverse("installment_pay_api", args=[installment.id])
    response = user_api_client.post(url)
    assert response.status_code == 404
