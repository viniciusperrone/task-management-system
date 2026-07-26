import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


User = get_user_model()


@pytest.mark.django_db
class TestRegisterView:
    url = reverse("auth_register")

    def test_register_user_success(self, api_client, user_data):
        response = api_client.post(self.url, user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "tokens" in response.data
        assert response.data["tokens"]["access"] is not None
        assert response.data["tokens"]["refresh"] is not None
        assert User.objects.filter(email=user_data["email"]).exists()

    def test_register_user_duplicate_email_fails(self, api_client, user, user_data):
        user_data["username"] = "other_user"
        response = api_client.post(self.url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data


@pytest.mark.django_db
class TestLoginView:
    url = reverse("auth_login")

    def test_login_success(self, api_client, user, user_data):
        login_payload = {
            "identifier": user_data["username"],
            "password": user_data["password"],
        }

        response = api_client.post(self.url, login_payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]

    def test_login_invalid_credentials_fails(self, api_client, user):
        login_payload = {
            "username": user.username,
            "password": "wrongpassword",
        }
        response = api_client.post(self.url, login_payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestUserMeView:
    url = reverse("user_me")

    def test_get_me_unauthenticated_fails(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_authenticated_success(self, auth_client, user):
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email

    def test_update_me_nickname_success(self, auth_client, user):
        payload = {"nickname": "new_nick"}
        response = auth_client.patch(self.url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nickname"] == "new_nick"
        user.refresh_from_db()
        assert user.nickname == "new_nick"
