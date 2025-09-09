"""
Serializers untuk screening-service.
"""
from rest_framework import serializers
from .models import Anamnesis


class AnamnesisSerializer(serializers.ModelSerializer):
    """Serializer untuk model Anamnesis."""
    
    class Meta:
        model = Anamnesis
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnamnesisSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian anamnesis."""
    participant_id = serializers.IntegerField(required=False)
    pos_date = serializers.DateField(required=False)
    keluhan_utama = serializers.CharField(required=False)
