from rest_framework import serializers
from tickets.models import Column, Board, Ticket


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
