import pytest

from django.urls import reverse
from rest_framework import status

from tickets.models import Message
from tickets.choices import Priority


@pytest.mark.django_db
class TestTicketViewSet:
    list_url = reverse("tickets:ticket-list")

    def test_create_ticket_success(self, auth_client_owner, board_setup, user_owner):
        payload = {
            "title": "Corrigir bug na tela de login",
            "column": board_setup["col_todo"].id,
            "priority": Priority.HIGHEST,
        }

        response = auth_client_owner.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["owner"] == user_owner.id
        assert response.data["title"] == payload["title"]

    def test_guest_user_cannot_see_unshared_ticket(self, auth_client_guest, ticket):
        response = auth_client_guest.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_move_ticket_column_success(self, auth_client_owner, ticket, board_setup):
        move_url = reverse("tickets:ticket-move-column", kwargs={"pk": ticket.pk})

        payload = {
            "to_column_id": board_setup["col_doing"].id,
            "info": "Iniciando o desenvolvimento",
        }

        response = auth_client_owner.post(move_url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        ticket.refresh_from_db()

        assert ticket.column_id == board_setup["col_doing"].id

    def test_share_ticket_success(
        self,
        auth_client_guest,
        auth_client_owner,
        ticket,
        user_guest,
    ):
        share_url = reverse(
            "tickets:ticket-share-ticket",
            kwargs={"pk": ticket.pk},
        )

        payload = {
            "user_ids": [user_guest.id],
        }

        share_response = auth_client_owner.post(
            share_url,
            payload,
            format="json",
        )

        assert share_response.status_code == status.HTTP_200_OK

        list_response = auth_client_guest.get(self.list_url)

        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data["results"]) == 1
        assert list_response.data["results"][0]["id"] == ticket.id


@pytest.mark.django_db
class TestMessageViewSet:
    list_url = reverse("tickets:message-list")

    def test_create_message_success(self, auth_client_owner, ticket):
        payload = {
            "ticket": ticket.id,
            "message": "Comentário de teste sobre a demanda",
        }

        response = auth_client_owner.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == payload["message"]
        assert response.data["is_edited"] is False

    def test_create_reply_message_success(
        self,
        auth_client_owner,
        ticket,
        user_owner,
    ):
        parent_msg = Message.objects.create(
            ticket=ticket,
            author=user_owner,
            message="Mensagem original",
        )

        payload = {
            "ticket": ticket.id,
            "message": "Respondendo à mensagem original",
            "reply": parent_msg.id,
        }

        response = auth_client_owner.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["reply"] == parent_msg.id
        assert response.data["reply_detail"]["id"] == parent_msg.id

    def test_unauthorized_user_cannot_comment_on_ticket(
        self,
        auth_client_guest,
        ticket,
    ):
        payload = {
            "ticket": ticket.id,
            "message": "Tentando comentar sem permissão",
        }

        response = auth_client_guest.post(self.list_url, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
