import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from tickets.models import Board, Column, Ticket

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_owner(db):
    return User.objects.create_user(
        username="owner_user",
        email="owner@test.com",
        password="Password123!",
        first_name="Owner",
        last_name="User",
    )


@pytest.fixture
def user_guest(db):
    return User.objects.create_user(
        username="guest_user",
        email="guest@test.com",
        password="Password123!",
        first_name="Guest",
        last_name="User",
    )


@pytest.fixture
def auth_client_owner(api_client, user_owner):
    api_client.force_authenticate(user=user_owner)
    return api_client


@pytest.fixture
def auth_client_guest(api_client, user_guest):
    api_client.force_authenticate(user=user_guest)
    return api_client


@pytest.fixture
def board_setup(db, user_owner):
    board = Board.objects.create(name="Projeto Kanban", owner=user_owner)
    col_todo = Column.objects.create(name="A Fazer", board=board, position=1)
    col_doing = Column.objects.create(name="Em Progresso", board=board, position=2)
    return {
        "board": board,
        "col_todo": col_todo,
        "col_doing": col_doing,
    }


@pytest.fixture
def ticket(db, user_owner, board_setup):
    return Ticket.objects.create(
        title="Desenvolver API",
        column=board_setup["col_todo"],
        owner=user_owner,
        priority=3,
    )