"""
Model untuk participant-service.
Menangani data peserta POS BINDU PTM.
"""
from django.db import models
from django.core.validators import RegexValidator


class Location(models.Model):
    """Model untuk lokasi (Desa/RT/RW)."""
    nama = models.CharField(max_length=100)
    jenis = models.CharField(
        max_length=20,
        choices=[
            ('Desa', 'Desa'),
            ('RT', 'RT'),
            ('RW', 'RW'),
        ]
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.jenis} {self.nama}"


class Participant(models.Model):
    """Model untuk peserta POS BINDU PTM."""
    
    # Data Identitas
    nik = models.CharField(
        max_length=16,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\d{16}$',
            message='NIK harus 16 digit angka'
        )]
    )
    nama_lengkap = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ]
    )
    
    # Data Alamat
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Data Kontak
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    bpjs = models.BooleanField(default=False)
    kontak_darurat = models.CharField(max_length=100, blank=True, null=True)
    no_hp_darurat = models.CharField(max_length=15, blank=True, null=True)
    
    # Data Pekerjaan
    pekerjaan = models.CharField(max_length=100, blank=True, null=True)
    
    # Data Kesehatan Dasar
    status_merokok = models.CharField(
        max_length=20,
        choices=[
            ('Tidak', 'Tidak'),
            ('Aktif', 'Aktif'),
            ('Eks', 'Eks'),
        ],
        default='Tidak'
    )
    status_alkohol = models.CharField(
        max_length=20,
        choices=[
            ('Tidak', 'Tidak'),
            ('Ya', 'Ya'),
        ],
        default='Tidak'
    )
    
    # Riwayat Kesehatan
    riwayat_dm = models.BooleanField(default=False)
    riwayat_hipertensi = models.BooleanField(default=False)
    riwayat_stroke = models.BooleanField(default=False)
    riwayat_jantung = models.BooleanField(default=False)
    riwayat_asma_copd = models.BooleanField(default=False)
    riwayat_ginjal = models.BooleanField(default=False)
    riwayat_keluarga_ptm = models.BooleanField(default=False)
    
    # Data Tambahan
    foto = models.ImageField(upload_to='participant_photos/', blank=True, null=True)
    catatan_khusus = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nik']),
            models.Index(fields=['nama_lengkap']),
            models.Index(fields=['desa']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.nama_lengkap} ({self.nik})"
    
    @property
    def umur(self):
        """Menghitung umur dalam tahun."""
        from datetime import date
        today = date.today()
        return today.year - self.tanggal_lahir.year - (
            (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day)
        )


class Visit(models.Model):
    """Model untuk kunjungan peserta."""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='visits')
    pos_date = models.DateField()
    lokasi = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    petugas_id = models.IntegerField()  # ID dari auth service
    verified_by = models.IntegerField(null=True, blank=True)  # ID verifikator
    status = models.CharField(
        max_length=20,
        choices=[
            ('Draft', 'Draft'),
            ('Verified', 'Verified'),
            ('Completed', 'Completed'),
        ],
        default='Draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-pos_date', '-created_at']
        indexes = [
            models.Index(fields=['participant', 'pos_date']),
            models.Index(fields=['pos_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Kunjungan {self.participant.nama_lengkap} - {self.pos_date}"
