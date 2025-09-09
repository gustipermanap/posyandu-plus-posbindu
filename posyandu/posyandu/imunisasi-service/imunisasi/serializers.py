"""
Serializers untuk imunisasi-service.
"""
from rest_framework import serializers
from .models import JadwalImunisasi, PencatatanImunisasi, ReminderImunisasi, VaksinStock


class JadwalImunisasiSerializer(serializers.ModelSerializer):
    """Serializer untuk model JadwalImunisasi."""
    
    class Meta:
        model = JadwalImunisasi
        fields = [
            'id', 'jenis_imunisasi', 'usia_minimal_bulan', 'usia_maksimal_bulan',
            'interval_hari', 'deskripsi', 'aktif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PencatatanImunisasiSerializer(serializers.ModelSerializer):
    """Serializer untuk model PencatatanImunisasi."""
    
    class Meta:
        model = PencatatanImunisasi
        fields = [
            'id', 'balita_id', 'posyandu_id', 'jenis_imunisasi', 'tanggal_pemberian',
            'usia_saat_imunisasi_bulan', 'status', 'alasan_tidak_diberikan',
            'lokasi_pemberian', 'petugas_pemberian', 'batch_vaksin',
            'tanggal_kedaluwarsa', 'efek_samping', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReminderImunisasiSerializer(serializers.ModelSerializer):
    """Serializer untuk model ReminderImunisasi."""
    
    class Meta:
        model = ReminderImunisasi
        fields = [
            'id', 'balita_id', 'posyandu_id', 'jenis_imunisasi', 'usia_saat_ini_bulan',
            'status', 'tanggal_reminder', 'prioritas', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VaksinStockSerializer(serializers.ModelSerializer):
    """Serializer untuk model VaksinStock."""
    
    class Meta:
        model = VaksinStock
        fields = [
            'id', 'jenis_vaksin', 'batch_number', 'tanggal_kedaluwarsa',
            'jumlah_stok', 'harga_per_dosis', 'supplier', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ImunisasiSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian imunisasi."""
    balita_id = serializers.IntegerField(required=False)
    jenis_imunisasi = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
