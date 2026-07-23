from rest_framework.permissions import IsAuthenticated

from tickets.models import Column
from tickets.serializers import (
    ColumnSerializer,
)


class ColumnViewSet():
    permission_classes = [IsAuthenticated]
    serializer_class = ColumnSerializer

    def get_queryset(self):
        return Column.objects.filter(board__owner=self.request.user)
