"""
Serializers untuk reporting-service.
"""
from rest_framework import serializers
from .models import ReportLog, ActivityLog, DashboardData


class ReportLogSerializer(serializers.ModelSerializer):
    """Serializer untuk model ReportLog."""
    
    class Meta:
        model = ReportLog
        fields = [
            'id', 'nama_laporan', 'jenis_laporan', 'tanggal_mulai', 'tanggal_akhir',
            'data_laporan', 'file_laporan', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer untuk model ActivityLog."""
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user_id', 'modul', 'jenis_aktivitas', 'deskripsi',
            'data_sebelum', 'data_sesudah', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DashboardDataSerializer(serializers.ModelSerializer):
    """Serializer untuk model DashboardData."""
    
    class Meta:
        model = DashboardData
        fields = [
            'id', 'data_dashboard', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportLogSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian report log."""
    jenis_laporan = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    tanggal_mulai = serializers.DateField(required=False)
    tanggal_akhir = serializers.DateField(required=False)
