from django.db.models import Model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tickets.models import Column, Board, Ticket, TicketColumnTransition
from tickets.serializers import (
    ColumnSerializer,
    BoardSerializer, TicketSerializer, TicketColumnTransitionSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user).prefetch_related('columns')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ColumnViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(owner=self.request.user).select_related('columns')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path="move")
    def move_column(self, request, pk=None):
        ticket = self.get_object()
        to_column_id = request.date.get("to_column_id")
        info = request.data.get("info", "")

        if not to_column_id:
            return Response(
                {"error": "The 'to_column_id' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            to_column = Column.objects.get(pk=to_column_id, board__owner=request.user)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Destination column not found or permission denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        transition_obj = TicketColumnTransition.execute_transition(
            ticket=ticket,
            to_column=to_column,
            author=request.user,
            info=info,
        )

        ticket.refresh_from_db()

        return Response(
            {
                "message": "Ticket move successfully",
                "ticket": TicketSerializer(ticket).data,
                "transition_id": transition_obj.id if transition_obj else None,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['get'], url_path="transitions")
    def list_transitions(self, request, pk=None):
        ticket = self.get_object()
        transitions = ticket.transitions.select_related('from_column', 'to_column', 'author').all()
        serializer = TicketColumnTransitionSerializer(transitions, many=True)

        return Response(serializer.data)
