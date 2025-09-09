"""
Serializers untuk rujukan-service.
"""
from rest_framework import serializers
from .models import FasilitasKesehatan, Rujukan, FollowUpRujukan, TemplateRujukan


class FasilitasKesehatanSerializer(serializers.ModelSerializer):
    """Serializer untuk model FasilitasKesehatan."""
    
    class Meta:
        model = FasilitasKesehatan
        fields = [
            'id', 'nama', 'jenis_fasilitas', 'level_fasilitas', 'alamat',
            'rt', 'rw', 'desa', 'kecamatan', 'kabupaten', 'provinsi',
            'kode_pos', 'no_telepon', 'no_fax', 'email', 'website',
            'latitude', 'longitude', 'pelayanan_anak', 'pelayanan_ibu_hamil',
            'pelayanan_imunisasi', 'pelayanan_kb', 'pelayanan_gizi',
            'pelayanan_lab', 'pelayanan_radiologi', 'pelayanan_ugd',
            'aktif', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RujukanSerializer(serializers.ModelSerializer):
    """Serializer untuk model Rujukan."""
    
    class Meta:
        model = Rujukan
        fields = [
            'id', 'pasien_id', 'posyandu_id', 'jenis_pasien', 'fasilitas_tujuan',
            'tanggal_rujukan', 'jam_rujukan', 'alasan_rujukan', 'diagnosis_awal',
            'prioritas', 'status', 'tanggal_tindak_lanjut', 'hasil_rujukan',
            'diagnosis_akhir', 'tindakan', 'obat', 'rekomendasi',
            'petugas_rujukan', 'dokter_penerima', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FollowUpRujukanSerializer(serializers.ModelSerializer):
    """Serializer untuk model FollowUpRujukan."""
    
    class Meta:
        model = FollowUpRujukan
        fields = [
            'id', 'rujukan', 'tanggal_follow_up', 'status', 'hasil_follow_up',
            'tindak_lanjut', 'petugas_follow_up', 'catatan', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TemplateRujukanSerializer(serializers.ModelSerializer):
    """Serializer untuk model TemplateRujukan."""
    
    class Meta:
        model = TemplateRujukan
        fields = [
            'id', 'nama_template', 'jenis_pasien', 'indikasi_rujukan',
            'template_rujukan', 'fasilitas_rekomendasi', 'aktif',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RujukanSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian rujukan."""
    pasien_id = serializers.IntegerField(required=False)
    jenis_pasien = serializers.CharField(required=False)
    posyandu_id = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
