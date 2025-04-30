import pytest
from rest_framework.test import APIClient

from apps.users import factories as user_factories


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """This method (fixture) will enable db access globally for all tests"""
    pass


@pytest.fixture
def merchant_user():
    return user_factories.UserFactory.create(
        name="merchant",
        email="merchant@bnpl.co",
        is_merchant=True,
        password="secret_pwd",
    )


@pytest.fixture
def user():
    return user_factories.UserFactory.create(
        name="merchant",
        email="user@bnpl.co",
        is_merchant=False,
        password="secret_pwd",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def merchant_user_api_client(merchant_user):
    api_client = APIClient()
    api_client.force_authenticate(user=merchant_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def user_api_client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
