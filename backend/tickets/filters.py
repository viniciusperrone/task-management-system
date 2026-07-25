from django_filters import rest_framework as filters
from tickets.models import Ticket


class TicketFilter(filters.FilterSet):
    board = filters.NumberFilter(field_name="column__board_id")
    column = filters.NumberFilter(field_name="column_id")

    priority = filters.NumberFilter(field_name="priority")
    priority_gte = filters.NumberFilter(field_name="priority", lookup_expr="gte")
    priority_lte = filters.NumberFilter(field_name="priority", lookup_expr="lte")

    due_date = filters.DateFilter(field_name="due_date")
    due_date_lte = filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_date_gte = filters.DateFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Ticket
        fields = ['column', 'board', 'priority', 'due_date', 'owner']
