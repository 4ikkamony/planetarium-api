import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse("user:user-create")
TOKEN_OBTAIN = reverse("user:token-obtain-pair")
TOKEN_VERIFY = reverse("user:token-verify")
TOKEN_REFRESH = reverse("user:token-refresh")
ME_URL = reverse("user:user-manage")


@pytest.fixture
def api_client_anonymous():
    return APIClient()


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        email="regular@user.com", password="testpass", is_staff=False
    )


@pytest.fixture
def api_client_logged_in(api_client_anonymous, user):
    api_client_anonymous.force_authenticate(user)
    return api_client_anonymous


@pytest.mark.django_db
def test_create_valid_user_success(api_client_anonymous):
    payload = {"email": "tes1t@test.com", "password": "testpass"}
    res = api_client_anonymous.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_201_CREATED
    user_obj = get_user_model().objects.get(**res.data)
    assert user_obj.check_password(payload["password"])
    assert "password" not in res.data


@pytest.mark.django_db
def test_user_exists(api_client_anonymous):
    payload = {"email": "test@test.com", "password": "testpass"}
    get_user_model().objects.create_user(**payload)

    res = api_client_anonymous.post(CREATE_USER_URL, payload)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_token_for_user(api_client_anonymous):
    payload = {"email": "test@test.com", "password": "test123"}
    get_user_model().objects.create_user(**payload)

    res = api_client_anonymous.post(TOKEN_OBTAIN, payload)
    assert "refresh" in res.data
    assert "access" in res.data
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_token_no_user(api_client_logged_in):
    payload = {"email": "test@test.com", "password": "test123"}
    res = api_client_logged_in.post(TOKEN_OBTAIN, payload)

    assert "access" not in res.data
    assert "refresh" not in res.data
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_token_missing_field(api_client_anonymous):
    res = api_client_anonymous.post(TOKEN_OBTAIN, {"email": 1, "password": ""})

    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_user_unauthorized(api_client_anonymous):
    res = api_client_anonymous.get(ME_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
