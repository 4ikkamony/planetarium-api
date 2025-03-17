import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.db import connection


@pytest.fixture(scope="session", autouse=True)
def enable_trigram_extension(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user():
    return get_user_model().objects.create_user(
        email="regular@user.com", password="testpass", is_staff=False
    )


@pytest.fixture
def staff_user():
    return get_user_model().objects.create_user(
        email="staff@user.com", password="testpass", is_staff=True
    )


@pytest.fixture
def api_client_staff(api_client, staff_user):
    api_client.force_authenticate(staff_user)
    return api_client


@pytest.fixture
def api_client_regular(api_client, regular_user):
    api_client.force_authenticate(regular_user)
    return api_client
