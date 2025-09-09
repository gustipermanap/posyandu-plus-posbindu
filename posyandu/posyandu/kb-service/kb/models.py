"""
Model untuk kb-service.
Menangani KB & kesehatan reproduksi.
"""
from django.db import models
from decimal import Decimal


class MetodeKB(models.Model):
    """Model untuk metode KB yang tersedia."""
    
    # Jenis metode KB
    JENIS_METODE_CHOICES = [
        ('pil', 'Pil KB'),
        ('suntik', 'Suntik KB'),
        ('iud', 'IUD'),
        ('implant', 'Implant'),
        ('kondom', 'Kondom'),
        ('mow', 'MOW (Mengikat Saluran Telur)'),
        ('mop', 'MOP (Mengikat Saluran Sperma)'),
        ('laktasi', 'Laktasi'),
        ('kalender', 'Kalender'),
        ('spermatisida', 'Spermatisida'),
        ('diafragma', 'Diafragma'),
        ('cervical_cap', 'Cervical Cap'),
    ]
    
    jenis_metode = models.CharField(
        max_length=20,
        choices=JENIS_METODE_CHOICES,
        unique=True
    )
    
    # Deskripsi metode
    deskripsi = models.TextField(
        blank=True,
        null=True,
        help_text="Deskripsi metode KB"
    )
    
    # Efektivitas
    efektivitas_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Efektivitas dalam persen"
    )
    
    # Durasi perlindungan
    durasi_perlindungan_hari = models.IntegerField(
        null=True,
        blank=True,
        help_text="Durasi perlindungan dalam hari"
    )
    
    # Kontraindikasi
    kontraindikasi = models.TextField(
        blank=True,
        null=True,
        help_text="Kontraindikasi metode KB"
    )
    
    # Efek samping
    efek_samping = models.TextField(
        blank=True,
        null=True,
        help_text="Efek samping yang mungkin terjadi"
    )
    
    # Status aktif
    aktif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['jenis_metode']
        indexes = [
            models.Index(fields=['jenis_metode']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return self.get_jenis_metode_display()


class PencatatanKB(models.Model):
    """Model untuk pencatatan penggunaan KB."""
    
    # Data WUS
    wus_id = models.IntegerField()  # ID WUS
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Metode KB
    metode_kb = models.CharField(
        max_length=20,
        choices=MetodeKB.JENIS_METODE_CHOICES
    )
    
    # Tanggal mulai KB
    tanggal_mulai = models.DateField()
    
    # Tanggal berakhir KB
    tanggal_berakhir = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal berakhir KB (jika ada)"
    )
    
    # Status KB
    status = models.CharField(
        max_length=20,
        choices=[
            ('aktif', 'Aktif'),
            ('tidak_aktif', 'Tidak Aktif'),
            ('ganti_metode', 'Ganti Metode'),
            ('hamil', 'Hamil'),
            ('menolak', 'Menolak'),
        ],
        default='aktif'
    )
    
    # Alasan tidak aktif
    alasan_tidak_aktif = models.TextField(
        blank=True,
        null=True,
        help_text="Alasan jika tidak aktif KB"
    )
    
    # Efek samping yang dialami
    efek_samping = models.TextField(
        blank=True,
        null=True,
        help_text="Efek samping yang dialami"
    )
    
    # Kontrol ulang
    tanggal_kontrol_ulang = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal kontrol ulang"
    )
    
    # Petugas
    petugas_kb = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas KB"
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
        ordering = ['-tanggal_mulai']
        indexes = [
            models.Index(fields=['wus_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['metode_kb']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_mulai']),
        ]
    
    def __str__(self):
        return f"{self.get_metode_kb_display()} - {self.wus_id} - {self.tanggal_mulai}"


class KonselingKB(models.Model):
    """Model untuk konseling KB."""
    
    # Data WUS
    wus_id = models.IntegerField()  # ID WUS
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal konseling
    tanggal_konseling = models.DateField()
    
    # Jenis konseling
    jenis_konseling = models.CharField(
        max_length=20,
        choices=[
            ('awal', 'Konseling Awal'),
            ('kontrol', 'Kontrol Ulang'),
            ('ganti_metode', 'Ganti Metode'),
            ('efek_samping', 'Efek Samping'),
            ('hamil', 'Konseling Kehamilan'),
        ],
        default='awal'
    )
    
    # Topik konseling
    topik_konseling = models.TextField(
        help_text="Topik yang dibahas dalam konseling"
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi dari konseling"
    )
    
    # Metode KB yang direkomendasikan
    metode_direkomendasikan = models.CharField(
        max_length=20,
        choices=MetodeKB.JENIS_METODE_CHOICES,
        blank=True,
        null=True
    )
    
    # Status konseling
    status = models.CharField(
        max_length=20,
        choices=[
            ('selesai', 'Selesai'),
            ('tindak_lanjut', 'Tindak Lanjut'),
            ('rujukan', 'Rujukan'),
        ],
        default='selesai'
    )
    
    # Petugas konseling
    petugas_konseling = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas konseling"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan konseling"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_konseling']
        indexes = [
            models.Index(fields=['wus_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_konseling']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Konseling {self.get_jenis_konseling_display()} - {self.wus_id} - {self.tanggal_konseling}"


class StokKB(models.Model):
    """Model untuk stok alat KB."""
    
    # Jenis alat KB
    jenis_alat = models.CharField(
        max_length=50,
        help_text="Jenis alat KB"
    )
    
    # Metode KB
    metode_kb = models.CharField(
        max_length=20,
        choices=MetodeKB.JENIS_METODE_CHOICES
    )
    
    # Batch
    batch_number = models.CharField(
        max_length=50,
        help_text="Nomor batch"
    )
    
    # Tanggal kedaluwarsa
    tanggal_kedaluwarsa = models.DateField()
    
    # Jumlah stok
    jumlah_stok = models.IntegerField(help_text="Jumlah alat KB tersisa")
    
    # Harga per unit
    harga_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Harga per unit"
    )
    
    # Supplier
    supplier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama supplier"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('tersedia', 'Tersedia'),
            ('habis', 'Habis'),
            ('kedaluwarsa', 'Kedaluwarsa'),
        ],
        default='tersedia'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['jenis_alat']),
            models.Index(fields=['metode_kb']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['tanggal_kedaluwarsa']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.jenis_alat} - Batch: {self.batch_number}"
    
    @property
    def is_expired(self):
        """Cek apakah alat KB sudah kedaluwarsa."""
        from datetime import date
        return self.tanggal_kedaluwarsa < date.today()
    
    @property
    def is_expiring_soon(self):
        """Cek apakah alat KB akan kedaluwarsa dalam 30 hari."""
        from datetime import date, timedelta
        return self.tanggal_kedaluwarsa <= date.today() + timedelta(days=30)
    
    def use_kb_item(self, jumlah=1):
        """Mengurangi jumlah stok alat KB."""
        if self.jumlah_stok >= jumlah:
            self.jumlah_stok -= jumlah
            if self.jumlah_stok == 0:
                self.status = 'habis'
            self.save()
            return True
        return False


class RujukanKB(models.Model):
    """Model untuk rujukan KB."""
    
    # Data WUS
    wus_id = models.IntegerField()  # ID WUS
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal rujukan
    tanggal_rujukan = models.DateField()
    
    # Tujuan rujukan
    tujuan_rujukan = models.CharField(
        max_length=100,
        help_text="Tujuan rujukan (Puskesmas, RS, dll)"
    )
    
    # Alasan rujukan
    alasan_rujukan = models.TextField(
        help_text="Alasan rujukan"
    )
    
    # Metode KB yang akan dipasang
    metode_kb = models.CharField(
        max_length=20,
        choices=MetodeKB.JENIS_METODE_CHOICES,
        blank=True,
        null=True
    )
    
    # Status rujukan
    status = models.CharField(
        max_length=20,
        choices=[
            ('dikirim', 'Dikirim'),
            ('diterima', 'Diterima'),
            ('selesai', 'Selesai'),
            ('ditolak', 'Ditolak'),
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
    
    # Petugas rujukan
    petugas_rujukan = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang merujuk"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan rujukan"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_rujukan']
        indexes = [
            models.Index(fields=['wus_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_rujukan']),
        ]
    
    def __str__(self):
        return f"Rujukan KB - {self.wus_id} - {self.tanggal_rujukan}"
