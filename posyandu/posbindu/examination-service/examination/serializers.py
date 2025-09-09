"""
Serializers untuk examination-service.
"""
from rest_framework import serializers
from .models import VitalSigns, Anthropometry


class VitalSignsSerializer(serializers.ModelSerializer):
    """Serializer untuk model VitalSigns."""
    
    class Meta:
        model = VitalSigns
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnthropometrySerializer(serializers.ModelSerializer):
    """Serializer untuk model Anthropometry."""
    
    class Meta:
        model = Anthropometry
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class VitalSignsSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian vital signs."""
    visit_id = serializers.IntegerField(required=False)
    sistol_min = serializers.IntegerField(required=False)
    sistol_max = serializers.IntegerField(required=False)
    diastol_min = serializers.IntegerField(required=False)
    diastol_max = serializers.IntegerField(required=False)
