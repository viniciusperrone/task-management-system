from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from tickets.models import Column, Board, Ticket, Message, TicketColumnTransition
from tickets.filters import TicketFilter
from tickets.serializers import (
    ColumnSerializer,
    BoardSerializer,
    TicketSerializer,
    TicketColumnTransitionSerializer,
    TicketShareSerializer,
    MessageReplySummarySerializer,
    MessageSerializer,
)


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user).prefetch_related('columns__tickets')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ColumnViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TicketFilter
    search_fields = ['title', 'description', 'number']
    ordering_fields = ['priority', 'due_date', 'created_at', 'position']
    ordering = ['-priority', 'created_at']

    def get_queryset(self):
        return (
            Ticket.objects.filter(owner=self.request.user)
            | Ticket.objects.filter(shared_users=self.request.user)
        ).distinct().select_related('column', 'owner')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path="share")
    def share_ticket(self, request, pk=None):
        ticket = self.get_object()

        if ticket.owner != request.user:
            return Response(
                {"error": "Apenas o criador do ticket pode gerenciar o acesso."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TicketShareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = serializer.validated_data["user_ids"]

        if ticket.owner.id in user_ids:
            user_ids.remove(ticket.owner.id)

        return Response(
            {
                "message": "Permissões de acesso atualizadas com sucesso.",
                "shared_users": list(
                    ticket.shared_users.values("id", "username", "email")
                ),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], url_path="move")
    def move_column(self, request, pk=None):
        ticket = self.get_object()
        to_column_id = request.data.get("to_column_id")
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


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = MessageSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["ticket"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        accessible_tickets = (
            Ticket.objects.filter(owner=user) | Ticket.objects.filter(shared_users=user)
        ).values_list("id", flat=True)

        return (
            Message.objects.filter(ticket_id__in=accessible_tickets)
            .select_related("author", "reply", "reply__author", "ticket")
        )

    def perform_create(self, serializer):
        ticket = serializer.validated_data["ticket"]
        user = self.request.user

        is_owner = ticket.owner_id == user.id
        is_shared = ticket.shared_users.filter(id=user.id).exists()

        if not (is_owner or is_shared):
            raise PermissionDenied("Você não tem acesso a este ticket para enviar mensagens.")

        serializer.save(author=user)
