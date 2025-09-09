"""
Serializers untuk lab-service.
"""
from rest_framework import serializers
from .models import LabResult, Stock


class LabResultSerializer(serializers.ModelSerializer):
    """Serializer untuk model LabResult."""
    
    class Meta:
        model = LabResult
        fields = [
            'id', 'visit', 'jenis_pemeriksaan', 'hasil', 'nilai_normal',
            'status', 'catatan', 'tanggal_pemeriksaan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    """Serializer untuk model Stock."""
    
    class Meta:
        model = Stock
        fields = [
            'id', 'nama_item', 'jenis_item', 'stok_awal', 'stok_tersisa',
            'satuan', 'tanggal_kadaluarsa', 'supplier', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LabResultSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian lab result."""
    visit_id = serializers.IntegerField(required=False)
    jenis_pemeriksaan = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
