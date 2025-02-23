import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse("user:user-create")
TOKEN_OBTAIN = reverse("user:token-obtain-pair")
TOKEN_VERIFY = reverse("user:token-verify")
TOKEN_REFRESH = reverse("user:token-refresh")
ME_URL = reverse("user:user-manage")


@pytest.mark.django_db
class TestUserAPI:

    def test_create_valid_user_success(self, api_client):
        payload = {"email": "tes1t@test.com", "password": "testpass"}
        res = api_client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_201_CREATED
        user_obj = get_user_model().objects.get(**res.data)
        assert user_obj.check_password(payload["password"])
        assert "password" not in res.data

    def test_user_exists(self, api_client):
        payload = {"email": "test@test.com", "password": "testpass"}
        get_user_model().objects.create_user(**payload)

        res = api_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_token_for_user(self, api_client):
        payload = {"email": "test@test.com", "password": "test123"}
        get_user_model().objects.create_user(**payload)

        res = api_client.post(TOKEN_OBTAIN, payload)
        assert "refresh" in res.data
        assert "access" in res.data
        assert res.status_code == status.HTTP_200_OK

    def test_create_token_no_user(self, api_client_regular):
        payload = {"email": "test@test.com", "password": "test123"}
        res = api_client_regular.post(TOKEN_OBTAIN, payload)

        assert "access" not in res.data
        assert "refresh" not in res.data
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_token_missing_field(self, api_client):
        res = api_client.post(TOKEN_OBTAIN, {"email": 1, "password": ""})

        assert "token" not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_user_unauthorized(self, api_client):
        res = api_client.get(ME_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
