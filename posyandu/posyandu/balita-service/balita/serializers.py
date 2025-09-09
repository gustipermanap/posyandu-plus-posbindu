"""
Serializers untuk balita-service.
"""
from rest_framework import serializers
from .models import PemeriksaanBalita, ImunisasiBalita, VitaminBalita


class PemeriksaanBalitaSerializer(serializers.ModelSerializer):
    """Serializer untuk model PemeriksaanBalita."""
    
    class Meta:
        model = PemeriksaanBalita
        fields = [
            'id', 'visit_id', 'balita_id', 'posyandu_id', 'tanggal_pemeriksaan',
            'berat_badan', 'tinggi_badan', 'lingkar_kepala', 'lingkar_lengan',
            'status_gizi', 'motorik_kasar', 'motorik_halus', 'bicara', 'sosial',
            'catatan_perkembangan', 'rekomendasi', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ImunisasiBalitaSerializer(serializers.ModelSerializer):
    """Serializer untuk model ImunisasiBalita."""
    
    class Meta:
        model = ImunisasiBalita
        fields = [
            'id', 'balita_id', 'posyandu_id', 'jenis_imunisasi', 'tanggal_imunisasi',
            'usia_saat_imunisasi', 'status', 'alasan_tidak_diberikan', 'lokasi_imunisasi',
            'petugas_imunisasi', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VitaminBalitaSerializer(serializers.ModelSerializer):
    """Serializer untuk model VitaminBalita."""
    
    class Meta:
        model = VitaminBalita
        fields = [
            'id', 'balita_id', 'posyandu_id', 'jenis_vitamin', 'tanggal_pemberian',
            'dosis', 'status', 'alasan_tidak_diberikan', 'petugas_pemberian',
            'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BalitaSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian balita."""
    nik = serializers.CharField(required=False)
    nama = serializers.CharField(required=False)
    nama_ibu = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
