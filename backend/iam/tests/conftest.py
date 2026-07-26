import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        "username": "joao.silva",
        "email": "joao@orizon.com",
        "password": "Password123!",
        "first_name": "João",
        "last_name": "Silva",
        "nickname": "Jota"
    }

@pytest.fixture
def user(db, user_data):
    return User.objects.create_user(**user_data)

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)

    return api_client
