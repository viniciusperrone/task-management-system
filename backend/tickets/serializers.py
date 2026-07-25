from rest_framework import serializers

from tickets.models import Column, Board, Ticket, TicketColumnTransition
from iam.models import User


class TicketColumnTransitionSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True, default="Sistema")
    from_column_name = serializers.CharField(source='from_column.name', read_only=True, default=None)
    to_column_name = serializers.CharField(source='to_column.name', read_only=True, default=None)

    class Meta:
        model = TicketColumnTransition
        fields = [
            'id',
            'ticket',
            'from_column',
            'from_column_name',
            'to_column',
            'to_column_name',
            'author',
            'author_username',
            'info',
            'created_at',
        ]
        read_only_fields = fields


class TicketShareSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        help_text="Lista de IDs dos usuários que terão acesso ao ticket."
    )

    def validate_user_ids(self, value):
        existing_ids = set(
            User.objects.filter(id__in=value).values_list("id", flat=True)
        )
        invalid_ids = set(value) - existing_ids

        if invalid_ids:
            raise serializers.ValidationError(
                f"Usuários com os IDs {list(invalid_ids)} não foram encontrados."
            )

        return value


class TicketSerializer(serializers.ModelSerializer):
    formatted_number = serializers.CharField(read_only=True)
    column_board_id = serializers.IntegerField(source="column.board.id", read_only=True, default=None)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'number',
            'formatted_number',
            'title',
            'description',
            'priority',
            'due_date',
            'column',
            'column_board_id',
            'position',
            'owner',
            'shared_users',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'number', 'formatted_number', 'position', 'owner', 'created_at', 'updated_at']


class ColumnSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ['id', 'name', 'position', 'color', 'board', 'tickets', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'color', 'owner', 'columns', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
