"""
Serializers untuk referral-service.
"""
from rest_framework import serializers
from .models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    """Serializer untuk model Referral."""
    
    class Meta:
        model = Referral
        fields = [
            'id', 'visit', 'fasilitas_tujuan', 'alasan_rujukan', 'prioritas',
            'status', 'tanggal_rujukan', 'tanggal_tindak_lanjut', 'hasil_rujukan',
            'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReferralSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian referral."""
    visit_id = serializers.IntegerField(required=False)
    fasilitas_tujuan = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    prioritas = serializers.CharField(required=False)
