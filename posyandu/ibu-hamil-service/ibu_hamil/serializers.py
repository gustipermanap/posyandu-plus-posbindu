"""
Serializers untuk ibu-hamil-service.
"""
from rest_framework import serializers
from .models import PemeriksaanIbuHamil, SuplemenIbuHamil, IbuNifas, BayiBaruLahir


class PemeriksaanIbuHamilSerializer(serializers.ModelSerializer):
    """Serializer untuk model PemeriksaanIbuHamil."""
    
    class Meta:
        model = PemeriksaanIbuHamil
        fields = [
            'id', 'visit_id', 'ibu_hamil_id', 'posyandu_id', 'tanggal_pemeriksaan',
            'usia_kehamilan_minggu', 'tekanan_darah_sistol', 'tekanan_darah_diastol',
            'nadi', 'tinggi_fundus', 'lingkar_lengan_atas', 'gerakan_janin',
            'hb', 'protein_urine', 'gula_darah', 'keluhan', 'risiko_tinggi',
            'jenis_risiko', 'rekomendasi', 'perlu_rujukan', 'alasan_rujukan',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SuplemenIbuHamilSerializer(serializers.ModelSerializer):
    """Serializer untuk model SuplemenIbuHamil."""
    
    class Meta:
        model = SuplemenIbuHamil
        fields = [
            'id', 'ibu_hamil_id', 'posyandu_id', 'jenis_suplemen', 'tanggal_pemberian',
            'dosis', 'jumlah', 'status', 'alasan_tidak_diberikan', 'petugas_pemberian',
            'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IbuNifasSerializer(serializers.ModelSerializer):
    """Serializer untuk model IbuNifas."""
    
    class Meta:
        model = IbuNifas
        fields = [
            'id', 'ibu_hamil_id', 'posyandu_id', 'tanggal_persalinan', 'jenis_persalinan',
            'tempat_persalinan', 'kondisi_ibu', 'keluhan', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BayiBaruLahirSerializer(serializers.ModelSerializer):
    """Serializer untuk model BayiBaruLahir."""
    
    class Meta:
        model = BayiBaruLahir
        fields = [
            'id', 'ibu_hamil_id', 'posyandu_id', 'tanggal_lahir', 'jam_lahir',
            'jenis_kelamin', 'berat_lahir', 'panjang_lahir', 'lingkar_kepala',
            'kondisi_lahir', 'apgar_1', 'apgar_5', 'imd', 'imunisasi_hb0',
            'status', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IbuHamilSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian ibu hamil."""
    nik = serializers.CharField(required=False)
    nama = serializers.CharField(required=False)
    nama_suami = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
