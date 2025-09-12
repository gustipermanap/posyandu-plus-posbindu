"""
Serializers untuk vitamin-service.
"""
from rest_framework import serializers
from .models import JenisVitamin, PemberianVitamin, PMT, StokVitamin, StokPMT


class JenisVitaminSerializer(serializers.ModelSerializer):
    """Serializer untuk model JenisVitamin."""
    
    class Meta:
        model = JenisVitamin
        fields = [
            'id', 'jenis_vitamin', 'deskripsi', 'dosis_harian_anak',
            'dosis_harian_dewasa', 'unit_dosis', 'indikasi', 'kontraindikasi',
            'efek_samping', 'aktif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PemberianVitaminSerializer(serializers.ModelSerializer):
    """Serializer untuk model PemberianVitamin."""
    
    class Meta:
        model = PemberianVitamin
        fields = [
            'id', 'penerima_id', 'posyandu_id', 'jenis_penerima', 'jenis_vitamin',
            'tanggal_pemberian', 'dosis', 'unit_dosis', 'status',
            'alasan_tidak_diberikan', 'petugas_pemberian', 'catatan',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PMTSerializer(serializers.ModelSerializer):
    """Serializer untuk model PMT."""
    
    class Meta:
        model = PMT
        fields = [
            'id', 'penerima_id', 'posyandu_id', 'jenis_penerima', 'jenis_pmt',
            'tanggal_pemberian', 'jumlah', 'unit_jumlah', 'status',
            'alasan_tidak_diberikan', 'petugas_pemberian', 'catatan',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StokVitaminSerializer(serializers.ModelSerializer):
    """Serializer untuk model StokVitamin."""
    
    class Meta:
        model = StokVitamin
        fields = [
            'id', 'jenis_vitamin', 'nama_produk', 'batch_number', 'tanggal_kedaluwarsa',
            'jumlah_stok', 'harga_per_unit', 'supplier', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StokPMTSerializer(serializers.ModelSerializer):
    """Serializer untuk model StokPMT."""
    
    class Meta:
        model = StokPMT
        fields = [
            'id', 'jenis_pmt', 'nama_produk', 'batch_number', 'tanggal_kedaluwarsa',
            'jumlah_stok', 'unit_stok', 'harga_per_unit', 'supplier', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VitaminSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian vitamin."""
    penerima_id = serializers.IntegerField(required=False)
    jenis_vitamin = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
