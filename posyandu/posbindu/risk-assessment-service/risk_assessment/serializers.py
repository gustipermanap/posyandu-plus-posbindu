"""
Serializers untuk risk-assessment-service.
"""
from rest_framework import serializers
from .models import RiskAssessment


class RiskAssessmentSerializer(serializers.ModelSerializer):
    """Serializer untuk model RiskAssessment."""
    
    class Meta:
        model = RiskAssessment
        fields = [
            'id', 'visit', 'jenis_penilaian', 'skor_total', 'kategori_risiko',
            'rekomendasi', 'tindak_lanjut', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiskAssessmentSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian risk assessment."""
    visit_id = serializers.IntegerField(required=False)
    jenis_penilaian = serializers.CharField(required=False)
    kategori_risiko = serializers.CharField(required=False)
