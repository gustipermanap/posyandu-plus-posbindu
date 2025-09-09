"""
Model untuk referral-service.
Menangani rujukan POS BINDU PTM.
"""
from django.db import models


class ReferralFacility(models.Model):
    """Model untuk fasilitas rujukan."""
    
    # Informasi fasilitas
    nama_fasilitas = models.CharField(max_length=200, help_text="Nama fasilitas rujukan")
    
    jenis_fasilitas = models.CharField(
        max_length=50,
        choices=[
            ('puskesmas', 'Puskesmas'),
            ('rumah_sakit', 'Rumah Sakit'),
            ('klinik', 'Klinik'),
            ('spesialis', 'Dokter Spesialis'),
            ('laboratorium', 'Laboratorium'),
        ]
    )
    
    # Alamat
    alamat = models.TextField(help_text="Alamat fasilitas")
    kota = models.CharField(max_length=100, help_text="Kota")
    provinsi = models.CharField(max_length=100, help_text="Provinsi")
    
    # Kontak
    no_telepon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Spesialisasi
    spesialisasi = models.TextField(
        blank=True,
        null=True,
        help_text="Spesialisasi yang tersedia"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('aktif', 'Aktif'),
            ('tidak_aktif', 'Tidak Aktif'),
        ],
        default='aktif'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['nama_fasilitas']
        indexes = [
            models.Index(fields=['jenis_fasilitas']),
            models.Index(fields=['kota']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.nama_fasilitas} - {self.get_jenis_fasilitas_display()}"


class Referral(models.Model):
    """Model untuk rujukan."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Fasilitas rujukan
    fasilitas_tujuan = models.ForeignKey(
        ReferralFacility,
        on_delete=models.CASCADE,
        help_text="Fasilitas tujuan rujukan"
    )
    
    # Informasi rujukan
    no_rujukan = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nomor surat rujukan"
    )
    
    tanggal_rujukan = models.DateField(help_text="Tanggal rujukan")
    
    # Alasan rujukan
    alasan_rujukan = models.TextField(help_text="Alasan rujukan")
    
    # Indikasi rujukan
    indikasi_rujukan = models.TextField(
        blank=True,
        null=True,
        help_text="Indikasi medis untuk rujukan"
    )
    
    # Ringkasan temuan
    ringkasan_temuan = models.TextField(
        help_text="Ringkasan temuan pemeriksaan"
    )
    
    # Instruksi khusus
    instruksi_khusus = models.TextField(
        blank=True,
        null=True,
        help_text="Instruksi khusus untuk fasilitas tujuan"
    )
    
    # Jadwal kontrol balik
    jadwal_kontrol_balik = models.DateField(
        blank=True,
        null=True,
        help_text="Jadwal kontrol balik"
    )
    
    # Status rujukan
    status_rujukan = models.CharField(
        max_length=20,
        choices=[
            ('dikirim', 'Dikirim'),
            ('diterima', 'Diterima'),
            ('diproses', 'Diproses'),
            ('selesai', 'Selesai'),
            ('ditolak', 'Ditolak'),
        ],
        default='dikirim'
    )
    
    # Tanggal diterima
    tanggal_diterima = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Tanggal rujukan diterima"
    )
    
    # Tanggal selesai
    tanggal_selesai = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Tanggal rujukan selesai"
    )
    
    # Hasil rujukan
    hasil_rujukan = models.TextField(
        blank=True,
        null=True,
        help_text="Hasil dari fasilitas tujuan"
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi dari fasilitas tujuan"
    )
    
    # File pendukung
    file_rujukan = models.FileField(
        upload_to='referral_files/',
        blank=True,
        null=True,
        help_text="File surat rujukan"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_rujukan']
        indexes = [
            models.Index(fields=['visit_id']),
            models.Index(fields=['participant_id']),
            models.Index(fields=['fasilitas_tujuan']),
            models.Index(fields=['no_rujukan']),
            models.Index(fields=['tanggal_rujukan']),
            models.Index(fields=['status_rujukan']),
        ]
    
    def __str__(self):
        return f"Rujukan {self.no_rujukan} - {self.fasilitas_tujuan.nama_fasilitas}"
    
    def generate_referral_number(self):
        """Generate nomor rujukan otomatis."""
        from datetime import datetime
        import random
        
        # Format: REF-YYYYMMDD-XXXX
        date_str = datetime.now().strftime('%Y%m%d')
        random_num = random.randint(1000, 9999)
        self.no_rujukan = f"REF-{date_str}-{random_num}"
        return self.no_rujukan


class ReferralFollowUp(models.Model):
    """Model untuk follow-up rujukan."""
    
    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )
    
    # Tanggal follow-up
    tanggal_follow_up = models.DateField()
    
    # Metode follow-up
    METODE_CHOICES = [
        ('telepon', 'Telepon'),
        ('whatsapp', 'WhatsApp'),
        ('kunjungan', 'Kunjungan'),
        ('email', 'Email'),
    ]
    
    metode_follow_up = models.CharField(
        max_length=20,
        choices=METODE_CHOICES
    )
    
    # Hasil follow-up
    hasil_follow_up = models.TextField(help_text="Hasil follow-up")
    
    # Status tindak lanjut
    status_tindak_lanjut = models.CharField(
        max_length=20,
        choices=[
            ('belum_dilakukan', 'Belum Dilakukan'),
            ('sedang_dilakukan', 'Sedang Dilakukan'),
            ('sudah_dilakukan', 'Sudah Dilakukan'),
            ('tidak_perlu', 'Tidak Perlu'),
        ]
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan tambahan"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_follow_up']
        indexes = [
            models.Index(fields=['referral']),
            models.Index(fields=['tanggal_follow_up']),
            models.Index(fields=['metode_follow_up']),
            models.Index(fields=['status_tindak_lanjut']),
        ]
    
    def __str__(self):
        return f"Follow-up {self.referral.no_rujukan} - {self.tanggal_follow_up}"
