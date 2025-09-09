"""
Serializers untuk kb-service.
"""
from rest_framework import serializers
from .models import MetodeKB, PencatatanKB, KonselingKB, StokKB, RujukanKB


class MetodeKBSerializer(serializers.ModelSerializer):
    """Serializer untuk model MetodeKB."""
    
    class Meta:
        model = MetodeKB
        fields = [
            'id', 'jenis_metode', 'deskripsi', 'efektivitas_percent',
            'durasi_perlindungan_hari', 'kontraindikasi', 'efek_samping',
            'aktif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PencatatanKBSerializer(serializers.ModelSerializer):
    """Serializer untuk model PencatatanKB."""
    
    class Meta:
        model = PencatatanKB
        fields = [
            'id', 'wus_id', 'posyandu_id', 'metode_kb', 'tanggal_mulai',
            'tanggal_berakhir', 'status', 'alasan_tidak_aktif', 'efek_samping',
            'tanggal_kontrol_ulang', 'petugas_kb', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class KonselingKBSerializer(serializers.ModelSerializer):
    """Serializer untuk model KonselingKB."""
    
    class Meta:
        model = KonselingKB
        fields = [
            'id', 'wus_id', 'posyandu_id', 'tanggal_konseling', 'jenis_konseling',
            'topik_konseling', 'rekomendasi', 'metode_direkomendasikan', 'status',
            'petugas_konseling', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StokKBSerializer(serializers.ModelSerializer):
    """Serializer untuk model StokKB."""
    
    class Meta:
        model = StokKB
        fields = [
            'id', 'jenis_alat', 'metode_kb', 'batch_number', 'tanggal_kedaluwarsa',
            'jumlah_stok', 'harga_per_unit', 'supplier', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RujukanKBSerializer(serializers.ModelSerializer):
    """Serializer untuk model RujukanKB."""
    
    class Meta:
        model = RujukanKB
        fields = [
            'id', 'wus_id', 'posyandu_id', 'tanggal_rujukan', 'tujuan_rujukan',
            'alasan_rujukan', 'metode_kb', 'status', 'tanggal_tindak_lanjut',
            'hasil_rujukan', 'petugas_rujukan', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class KBSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian KB."""
    wus_id = serializers.IntegerField(required=False)
    metode_kb = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
