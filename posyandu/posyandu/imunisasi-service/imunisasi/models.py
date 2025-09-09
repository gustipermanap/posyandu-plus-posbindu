"""
Model untuk imunisasi-service.
Menangani jadwal dan pencatatan imunisasi balita.
"""
from django.db import models
from decimal import Decimal


class JadwalImunisasi(models.Model):
    """Model untuk jadwal imunisasi berdasarkan usia."""
    
    # Jenis imunisasi
    JENIS_IMUNISASI_CHOICES = [
        ('bcg', 'BCG'),
        ('polio_0', 'Polio 0'),
        ('polio_1', 'Polio 1'),
        ('polio_2', 'Polio 2'),
        ('polio_3', 'Polio 3'),
        ('polio_4', 'Polio 4'),
        ('dpt_1', 'DPT 1'),
        ('dpt_2', 'DPT 2'),
        ('dpt_3', 'DPT 3'),
        ('hepb_1', 'HepB 1'),
        ('hepb_2', 'HepB 2'),
        ('hepb_3', 'HepB 3'),
        ('campak', 'Campak'),
        ('mr_1', 'MR 1'),
        ('mr_2', 'MR 2'),
        ('dt', 'DT'),
        ('tt', 'TT'),
    ]
    
    jenis_imunisasi = models.CharField(
        max_length=20,
        choices=JENIS_IMUNISASI_CHOICES,
        unique=True
    )
    
    # Usia pemberian
    usia_minimal_bulan = models.IntegerField(help_text="Usia minimal dalam bulan")
    usia_maksimal_bulan = models.IntegerField(help_text="Usia maksimal dalam bulan")
    
    # Interval dengan imunisasi sebelumnya
    interval_hari = models.IntegerField(
        null=True,
        blank=True,
        help_text="Interval minimal dengan imunisasi sebelumnya (hari)"
    )
    
    # Deskripsi
    deskripsi = models.TextField(
        blank=True,
        null=True,
        help_text="Deskripsi imunisasi"
    )
    
    # Status aktif
    aktif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['usia_minimal_bulan', 'jenis_imunisasi']
        indexes = [
            models.Index(fields=['jenis_imunisasi']),
            models.Index(fields=['usia_minimal_bulan']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_imunisasi_display()} - {self.usia_minimal_bulan}-{self.usia_maksimal_bulan} bulan"


class PencatatanImunisasi(models.Model):
    """Model untuk pencatatan imunisasi yang sudah diberikan."""
    
    # Data balita
    balita_id = models.IntegerField()  # ID balita
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Jenis imunisasi
    jenis_imunisasi = models.CharField(
        max_length=20,
        choices=JadwalImunisasi.JENIS_IMUNISASI_CHOICES
    )
    
    # Tanggal pemberian
    tanggal_pemberian = models.DateField()
    
    # Usia saat imunisasi
    usia_saat_imunisasi_bulan = models.IntegerField(help_text="Usia saat imunisasi dalam bulan")
    
    # Status pemberian
    status = models.CharField(
        max_length=20,
        choices=[
            ('diberikan', 'Diberikan'),
            ('tidak_diberikan', 'Tidak Diberikan'),
            ('kontraindikasi', 'Kontraindikasi'),
            ('menolak', 'Menolak'),
        ],
        default='diberikan'
    )
    
    # Alasan tidak diberikan
    alasan_tidak_diberikan = models.TextField(
        blank=True,
        null=True,
        help_text="Alasan jika tidak diberikan"
    )
    
    # Lokasi pemberian
    lokasi_pemberian = models.CharField(
        max_length=100,
        choices=[
            ('posyandu', 'Posyandu'),
            ('puskesmas', 'Puskesmas'),
            ('rumah_sakit', 'Rumah Sakit'),
            ('klinik', 'Klinik'),
            ('rumah', 'Rumah'),
        ],
        default='posyandu'
    )
    
    # Petugas
    petugas_pemberian = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang memberikan imunisasi"
    )
    
    # Batch vaksin
    batch_vaksin = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Nomor batch vaksin"
    )
    
    # Tanggal kedaluwarsa vaksin
    tanggal_kedaluwarsa = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal kedaluwarsa vaksin"
    )
    
    # Efek samping
    efek_samping = models.TextField(
        blank=True,
        null=True,
        help_text="Efek samping yang terjadi"
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
        ordering = ['-tanggal_pemberian']
        indexes = [
            models.Index(fields=['balita_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_imunisasi']),
            models.Index(fields=['tanggal_pemberian']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_imunisasi_display()} - {self.balita_id} - {self.tanggal_pemberian}"


class ReminderImunisasi(models.Model):
    """Model untuk reminder imunisasi yang belum lengkap."""
    
    # Data balita
    balita_id = models.IntegerField()  # ID balita
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Jenis imunisasi yang belum
    jenis_imunisasi = models.CharField(
        max_length=20,
        choices=JadwalImunisasi.JENIS_IMUNISASI_CHOICES
    )
    
    # Usia saat ini
    usia_saat_ini_bulan = models.IntegerField(help_text="Usia saat ini dalam bulan")
    
    # Status reminder
    status = models.CharField(
        max_length=20,
        choices=[
            ('belum_jadwal', 'Belum Jadwal'),
            ('sudah_jadwal', 'Sudah Jadwal'),
            ('terlambat', 'Terlambat'),
            ('diberikan', 'Diberikan'),
        ],
        default='belum_jadwal'
    )
    
    # Tanggal reminder
    tanggal_reminder = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal reminder"
    )
    
    # Prioritas
    prioritas = models.CharField(
        max_length=20,
        choices=[
            ('rendah', 'Rendah'),
            ('sedang', 'Sedang'),
            ('tinggi', 'Tinggi'),
            ('urgent', 'Urgent'),
        ],
        default='sedang'
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan reminder"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['prioritas', '-tanggal_reminder']
        indexes = [
            models.Index(fields=['balita_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_imunisasi']),
            models.Index(fields=['status']),
            models.Index(fields=['prioritas']),
        ]
    
    def __str__(self):
        return f"Reminder {self.get_jenis_imunisasi_display()} - {self.balita_id}"


class VaksinStock(models.Model):
    """Model untuk stok vaksin."""
    
    # Jenis vaksin
    jenis_vaksin = models.CharField(
        max_length=50,
        help_text="Nama vaksin"
    )
    
    # Batch
    batch_number = models.CharField(
        max_length=50,
        help_text="Nomor batch"
    )
    
    # Tanggal kedaluwarsa
    tanggal_kedaluwarsa = models.DateField()
    
    # Jumlah stok
    jumlah_stok = models.IntegerField(help_text="Jumlah vaksin tersisa")
    
    # Harga per dosis
    harga_per_dosis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Harga per dosis"
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
            models.Index(fields=['jenis_vaksin']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['tanggal_kedaluwarsa']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.jenis_vaksin} - Batch: {self.batch_number}"
    
    @property
    def is_expired(self):
        """Cek apakah vaksin sudah kedaluwarsa."""
        from datetime import date
        return self.tanggal_kedaluwarsa < date.today()
    
    @property
    def is_expiring_soon(self):
        """Cek apakah vaksin akan kedaluwarsa dalam 30 hari."""
        from datetime import date, timedelta
        return self.tanggal_kedaluwarsa <= date.today() + timedelta(days=30)
    
    def use_vaccine(self, jumlah=1):
        """Mengurangi jumlah stok vaksin."""
        if self.jumlah_stok >= jumlah:
            self.jumlah_stok -= jumlah
            if self.jumlah_stok == 0:
                self.status = 'habis'
            self.save()
            return True
        return False
