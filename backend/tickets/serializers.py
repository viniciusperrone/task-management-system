from rest_framework import serializers
from tickets.models import Column, Board


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
