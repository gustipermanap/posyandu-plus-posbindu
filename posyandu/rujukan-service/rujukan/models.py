"""
Model untuk rujukan-service.
Menangani manajemen rujukan.
"""
from django.db import models
from decimal import Decimal


class FasilitasKesehatan(models.Model):
    """Model untuk fasilitas kesehatan yang dapat menerima rujukan."""
    
    # Jenis fasilitas
    JENIS_FASILITAS_CHOICES = [
        ('puskesmas', 'Puskesmas'),
        ('rumah_sakit', 'Rumah Sakit'),
        ('klinik', 'Klinik'),
        ('bidan', 'Bidan'),
        ('dokter_praktik', 'Dokter Praktik'),
        ('rumah_sakit_khusus', 'Rumah Sakit Khusus'),
    ]
    
    # Level fasilitas
    LEVEL_FASILITAS_CHOICES = [
        ('primer', 'Primer'),
        ('sekunder', 'Sekunder'),
        ('tersier', 'Tersier'),
    ]
    
    nama = models.CharField(max_length=200, help_text="Nama fasilitas kesehatan")
    jenis_fasilitas = models.CharField(
        max_length=20,
        choices=JENIS_FASILITAS_CHOICES
    )
    level_fasilitas = models.CharField(
        max_length=20,
        choices=LEVEL_FASILITAS_CHOICES
    )
    
    # Alamat
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True, null=True)
    kabupaten = models.CharField(max_length=100, blank=True, null=True)
    provinsi = models.CharField(max_length=100, blank=True, null=True)
    kode_pos = models.CharField(max_length=10, blank=True, null=True)
    
    # Kontak
    no_telepon = models.CharField(max_length=20, blank=True, null=True)
    no_fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Koordinat
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        help_text="Koordinat latitude"
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        help_text="Koordinat longitude"
    )
    
    # Pelayanan yang tersedia
    pelayanan_anak = models.BooleanField(default=False)
    pelayanan_ibu_hamil = models.BooleanField(default=False)
    pelayanan_imunisasi = models.BooleanField(default=False)
    pelayanan_kb = models.BooleanField(default=False)
    pelayanan_gizi = models.BooleanField(default=False)
    pelayanan_lab = models.BooleanField(default=False)
    pelayanan_radiologi = models.BooleanField(default=False)
    pelayanan_ugd = models.BooleanField(default=False)
    
    # Status
    aktif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama']
        indexes = [
            models.Index(fields=['jenis_fasilitas']),
            models.Index(fields=['level_fasilitas']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return f"{self.nama} - {self.get_jenis_fasilitas_display()}"


class Rujukan(models.Model):
    """Model untuk rujukan pasien."""
    
    # Data pasien
    pasien_id = models.IntegerField()  # ID balita, ibu hamil, atau WUS
    posyandu_id = models.IntegerField()  # ID posyandu
    jenis_pasien = models.CharField(
        max_length=20,
        choices=[
            ('balita', 'Balita'),
            ('ibu_hamil', 'Ibu Hamil'),
            ('wus', 'WUS'),
        ]
    )
    
    # Fasilitas tujuan
    fasilitas_tujuan = models.ForeignKey(
        FasilitasKesehatan,
        on_delete=models.CASCADE,
        related_name='rujukan'
    )
    
    # Tanggal rujukan
    tanggal_rujukan = models.DateField()
    jam_rujukan = models.TimeField(blank=True, null=True)
    
    # Alasan rujukan
    alasan_rujukan = models.TextField(help_text="Alasan rujukan")
    diagnosis_awal = models.TextField(
        blank=True,
        null=True,
        help_text="Diagnosis awal dari posyandu"
    )
    
    # Prioritas rujukan
    prioritas = models.CharField(
        max_length=20,
        choices=[
            ('rendah', 'Rendah'),
            ('sedang', 'Sedang'),
            ('tinggi', 'Tinggi'),
            ('darurat', 'Darurat'),
        ],
        default='sedang'
    )
    
    # Status rujukan
    status = models.CharField(
        max_length=20,
        choices=[
            ('dikirim', 'Dikirim'),
            ('diterima', 'Diterima'),
            ('dalam_proses', 'Dalam Proses'),
            ('selesai', 'Selesai'),
            ('ditolak', 'Ditolak'),
            ('batal', 'Batal'),
        ],
        default='dikirim'
    )
    
    # Tanggal tindak lanjut
    tanggal_tindak_lanjut = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal tindak lanjut"
    )
    
    # Hasil rujukan
    hasil_rujukan = models.TextField(
        blank=True,
        null=True,
        help_text="Hasil dari rujukan"
    )
    diagnosis_akhir = models.TextField(
        blank=True,
        null=True,
        help_text="Diagnosis akhir dari fasilitas tujuan"
    )
    tindakan = models.TextField(
        blank=True,
        null=True,
        help_text="Tindakan yang dilakukan"
    )
    obat = models.TextField(
        blank=True,
        null=True,
        help_text="Obat yang diberikan"
    )
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi dari fasilitas tujuan"
    )
    
    # Petugas
    petugas_rujukan = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang merujuk"
    )
    dokter_penerima = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama dokter yang menerima rujukan"
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
        ordering = ['-tanggal_rujukan']
        indexes = [
            models.Index(fields=['pasien_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_pasien']),
            models.Index(fields=['status']),
            models.Index(fields=['prioritas']),
            models.Index(fields=['tanggal_rujukan']),
        ]
    
    def __str__(self):
        return f"Rujukan {self.get_jenis_pasien_display()} - {self.pasien_id} - {self.tanggal_rujukan}"


class FollowUpRujukan(models.Model):
    """Model untuk follow-up rujukan."""
    
    # Rujukan
    rujukan = models.ForeignKey(
        Rujukan,
        on_delete=models.CASCADE,
        related_name='follow_up'
    )
    
    # Tanggal follow-up
    tanggal_follow_up = models.DateField()
    
    # Status follow-up
    status = models.CharField(
        max_length=20,
        choices=[
            ('belum_datang', 'Belum Datang'),
            ('sudah_datang', 'Sudah Datang'),
            ('tidak_datang', 'Tidak Datang'),
            ('reschedule', 'Reschedule'),
        ],
        default='belum_datang'
    )
    
    # Hasil follow-up
    hasil_follow_up = models.TextField(
        blank=True,
        null=True,
        help_text="Hasil follow-up"
    )
    
    # Tindak lanjut
    tindak_lanjut = models.TextField(
        blank=True,
        null=True,
        help_text="Tindak lanjut yang diperlukan"
    )
    
    # Petugas follow-up
    petugas_follow_up = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang melakukan follow-up"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan follow-up"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_follow_up']
        indexes = [
            models.Index(fields=['rujukan']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_follow_up']),
        ]
    
    def __str__(self):
        return f"Follow-up {self.rujukan} - {self.tanggal_follow_up}"


class TemplateRujukan(models.Model):
    """Model untuk template rujukan."""
    
    # Nama template
    nama_template = models.CharField(max_length=100)
    
    # Jenis pasien
    jenis_pasien = models.CharField(
        max_length=20,
        choices=[
            ('balita', 'Balita'),
            ('ibu_hamil', 'Ibu Hamil'),
            ('wus', 'WUS'),
        ]
    )
    
    # Indikasi rujukan
    indikasi_rujukan = models.TextField(
        help_text="Indikasi untuk rujukan"
    )
    
    # Template rujukan
    template_rujukan = models.TextField(
        help_text="Template rujukan"
    )
    
    # Fasilitas yang direkomendasikan
    fasilitas_rekomendasi = models.ManyToManyField(
        FasilitasKesehatan,
        blank=True,
        help_text="Fasilitas yang direkomendasikan"
    )
    
    # Status
    aktif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama_template']
        indexes = [
            models.Index(fields=['jenis_pasien']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return f"{self.nama_template} - {self.get_jenis_pasien_display()}"
