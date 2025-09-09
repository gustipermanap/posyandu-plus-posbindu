"""
Serializers untuk intervention-service.
"""
from rest_framework import serializers
from .models import Intervention


class InterventionSerializer(serializers.ModelSerializer):
    """Serializer untuk model Intervention."""
    
    class Meta:
        model = Intervention
        fields = [
            'id', 'visit', 'jenis_intervensi', 'deskripsi', 'target',
            'metode', 'durasi', 'frekuensi', 'status', 'hasil',
            'evaluasi', 'tindak_lanjut', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InterventionSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian intervention."""
    visit_id = serializers.IntegerField(required=False)
    jenis_intervensi = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
