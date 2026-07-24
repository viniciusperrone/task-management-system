from rest_framework import serializers
from tickets.models import Column, Board, Ticket, TicketColumnTransition


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

    class Meta:
        model = Column
        fields = ['id', 'name', 'position', 'color', 'board', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'color', 'owner', 'columns', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
