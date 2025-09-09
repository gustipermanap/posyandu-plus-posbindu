"""
Serializers untuk participant-service.
"""
from rest_framework import serializers
from .models import Participant, Visit, Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer untuk model Location."""
    
    class Meta:
        model = Location
        fields = ['id', 'nama', 'jenis', 'parent']


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer untuk model Participant."""
    umur = serializers.ReadOnlyField()
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    
    class Meta:
        model = Participant
        fields = [
            'id', 'nik', 'nama_lengkap', 'tanggal_lahir', 'jenis_kelamin',
            'alamat', 'rt', 'rw', 'desa', 'desa_nama', 'no_hp', 'bpjs',
            'kontak_darurat', 'no_hp_darurat', 'pekerjaan', 'status_merokok',
            'status_alkohol', 'riwayat_dm', 'riwayat_hipertensi', 'riwayat_stroke',
            'riwayat_jantung', 'riwayat_asma_copd', 'riwayat_ginjal',
            'riwayat_keluarga_ptm', 'foto', 'catatan_khusus', 'umur',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'umur']
    
    def validate_nik(self, value):
        """Validasi NIK."""
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("NIK harus 16 digit angka")
        return value


class ParticipantListSerializer(serializers.ModelSerializer):
    """Serializer untuk list participant (ringkas)."""
    umur = serializers.ReadOnlyField()
    desa_nama = serializers.CharField(source='desa.nama', read_only=True)
    
    class Meta:
        model = Participant
        fields = [
            'id', 'nik', 'nama_lengkap', 'tanggal_lahir', 'jenis_kelamin',
            'alamat', 'rt', 'rw', 'desa_nama', 'no_hp', 'umur',
            'status_merokok', 'status_alkohol', 'created_at'
        ]


class VisitSerializer(serializers.ModelSerializer):
    """Serializer untuk model Visit."""
    participant_nama = serializers.CharField(source='participant.nama_lengkap', read_only=True)
    participant_nik = serializers.CharField(source='participant.nik', read_only=True)
    lokasi_nama = serializers.CharField(source='lokasi.nama', read_only=True)
    
    class Meta:
        model = Visit
        fields = [
            'id', 'participant', 'participant_nama', 'participant_nik',
            'pos_date', 'lokasi', 'lokasi_nama', 'petugas_id', 'verified_by',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ParticipantSearchSerializer(serializers.Serializer):
    """Serializer untuk pencarian participant."""
    nik = serializers.CharField(required=False)
    nama = serializers.CharField(required=False)
    no_hp = serializers.CharField(required=False)
    desa_id = serializers.IntegerField(required=False)
