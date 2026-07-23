from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from tickets.models import Column, Board
from tickets.serializers import (
    ColumnSerializer,
    BoardSerializer,
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
