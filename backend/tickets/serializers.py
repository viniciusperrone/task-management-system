from rest_framework import serializers
from tickets.models import Column


class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = ['id', 'name', 'position', 'color', 'board', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


