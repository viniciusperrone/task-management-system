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

