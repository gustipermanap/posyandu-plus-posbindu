"""
Serializers untuk laporan-service.
"""
from rest_framework import serializers
from .models import TemplateLaporan, Laporan, StatistikPosyandu, DashboardData, ExportLog


class TemplateLaporanSerializer(serializers.ModelSerializer):
    """Serializer untuk model TemplateLaporan."""
    
    class Meta:
        model = TemplateLaporan
        fields = [
            'id', 'nama_template', 'jenis_laporan', 'kategori_laporan',
            'template_laporan', 'query_sql', 'parameter_laporan', 'aktif',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LaporanSerializer(serializers.ModelSerializer):
    """Serializer untuk model Laporan."""
    
    class Meta:
        model = Laporan
        fields = [
            'id', 'template', 'posyandu_id', 'nama_laporan', 'tanggal_mulai',
            'tanggal_akhir', 'parameter_used', 'data_laporan', 'file_laporan',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StatistikPosyanduSerializer(serializers.ModelSerializer):
    """Serializer untuk model StatistikPosyandu."""
    
    class Meta:
        model = StatistikPosyandu
        fields = [
            'id', 'posyandu_id', 'tanggal_statistik', 'total_balita',
            'balita_gizi_normal', 'balita_gizi_kurang', 'balita_gizi_lebih',
            'balita_gizi_buruk', 'total_ibu_hamil', 'ibu_hamil_normal',
            'ibu_hamil_risiko_tinggi', 'total_imunisasi', 'imunisasi_lengkap',
            'imunisasi_tidak_lengkap', 'total_wus', 'wus_aktif_kb',
            'wus_tidak_aktif_kb', 'total_vitamin', 'total_pmt',
            'total_rujukan', 'rujukan_selesai', 'rujukan_pending',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardDataSerializer(serializers.ModelSerializer):
    """Serializer untuk model DashboardData."""
    
    class Meta:
        model = DashboardData
        fields = [
            'id', 'posyandu_id', 'tanggal_data', 'data_dashboard',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExportLogSerializer(serializers.ModelSerializer):
    """Serializer untuk model ExportLog."""
    
    class Meta:
        model = ExportLog
        fields = [
            'id', 'laporan', 'format_export', 'file_export', 'status',
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LaporanSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian laporan."""
    posyandu_id = serializers.IntegerField(required=False)
    jenis_laporan = serializers.CharField(required=False)
    kategori_laporan = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
