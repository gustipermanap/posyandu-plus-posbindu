"""
Serializers untuk posyandu-service.
"""
from rest_framework import serializers
from .models import Posyandu


class PosyanduSerializer(serializers.ModelSerializer):
    """Serializer untuk model Posyandu."""
    
    class Meta:
        model = Posyandu
        fields = ['id', 'nama', 'alamat']
        read_only_fields = ['id']
