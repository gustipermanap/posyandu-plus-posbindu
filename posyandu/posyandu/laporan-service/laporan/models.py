"""
Model untuk laporan-service.
Menangani laporan dan statistik.
"""
from django.db import models
from decimal import Decimal


class TemplateLaporan(models.Model):
    """Model untuk template laporan."""
    
    # Jenis laporan
    JENIS_LAPORAN_CHOICES = [
        ('harian', 'Laporan Harian'),
        ('mingguan', 'Laporan Mingguan'),
        ('bulanan', 'Laporan Bulanan'),
        ('tahunan', 'Laporan Tahunan'),
        ('khusus', 'Laporan Khusus'),
    ]
    
    # Kategori laporan
    KATEGORI_LAPORAN_CHOICES = [
        ('balita', 'Balita'),
        ('ibu_hamil', 'Ibu Hamil'),
        ('imunisasi', 'Imunisasi'),
        ('kb', 'KB'),
        ('vitamin', 'Vitamin & PMT'),
        ('rujukan', 'Rujukan'),
        ('umum', 'Umum'),
    ]
    
    nama_template = models.CharField(max_length=100)
    jenis_laporan = models.CharField(
        max_length=20,
        choices=JENIS_LAPORAN_CHOICES
    )
    kategori_laporan = models.CharField(
        max_length=20,
        choices=KATEGORI_LAPORAN_CHOICES
    )
    
    # Template laporan
    template_laporan = models.TextField(
        help_text="Template laporan dalam format HTML"
    )
    
    # Query SQL untuk data
    query_sql = models.TextField(
        blank=True,
        null=True,
        help_text="Query SQL untuk mengambil data"
    )
    
    # Parameter laporan
    parameter_laporan = models.JSONField(
        blank=True,
        null=True,
        help_text="Parameter yang diperlukan untuk laporan"
    )
    
    # Status
    aktif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama_template']
        indexes = [
            models.Index(fields=['jenis_laporan']),
            models.Index(fields=['kategori_laporan']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return f"{self.nama_template} - {self.get_jenis_laporan_display()}"


class Laporan(models.Model):
    """Model untuk laporan yang telah dibuat."""
    
    # Template laporan
    template = models.ForeignKey(
        TemplateLaporan,
        on_delete=models.CASCADE,
        related_name='laporan'
    )
    
    # Data laporan
    posyandu_id = models.IntegerField()  # ID posyandu
    nama_laporan = models.CharField(max_length=200)
    
    # Periode laporan
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField()
    
    # Parameter yang digunakan
    parameter_used = models.JSONField(
        blank=True,
        null=True,
        help_text="Parameter yang digunakan untuk membuat laporan"
    )
    
    # Data laporan
    data_laporan = models.JSONField(
        help_text="Data laporan dalam format JSON"
    )
    
    # File laporan
    file_laporan = models.FileField(
        upload_to='laporan/',
        blank=True,
        null=True,
        help_text="File laporan (PDF, Excel, dll)"
    )
    
    # Status laporan
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('final', 'Final'),
            ('published', 'Published'),
            ('archived', 'Archived'),
        ],
        default='draft'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_mulai']),
            models.Index(fields=['tanggal_akhir']),
        ]
    
    def __str__(self):
        return f"{self.nama_laporan} - {self.tanggal_mulai} s/d {self.tanggal_akhir}"


class StatistikPosyandu(models.Model):
    """Model untuk statistik posyandu."""
    
    # Data posyandu
    posyandu_id = models.IntegerField()  # ID posyandu
    tanggal_statistik = models.DateField()
    
    # Statistik balita
    total_balita = models.IntegerField(default=0)
    balita_gizi_normal = models.IntegerField(default=0)
    balita_gizi_kurang = models.IntegerField(default=0)
    balita_gizi_lebih = models.IntegerField(default=0)
    balita_gizi_buruk = models.IntegerField(default=0)
    
    # Statistik ibu hamil
    total_ibu_hamil = models.IntegerField(default=0)
    ibu_hamil_normal = models.IntegerField(default=0)
    ibu_hamil_risiko_tinggi = models.IntegerField(default=0)
    
    # Statistik imunisasi
    total_imunisasi = models.IntegerField(default=0)
    imunisasi_lengkap = models.IntegerField(default=0)
    imunisasi_tidak_lengkap = models.IntegerField(default=0)
    
    # Statistik KB
    total_wus = models.IntegerField(default=0)
    wus_aktif_kb = models.IntegerField(default=0)
    wus_tidak_aktif_kb = models.IntegerField(default=0)
    
    # Statistik vitamin
    total_vitamin = models.IntegerField(default=0)
    total_pmt = models.IntegerField(default=0)
    
    # Statistik rujukan
    total_rujukan = models.IntegerField(default=0)
    rujukan_selesai = models.IntegerField(default=0)
    rujukan_pending = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-tanggal_statistik']
        indexes = [
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_statistik']),
        ]
        unique_together = ['posyandu_id', 'tanggal_statistik']
    
    def __str__(self):
        return f"Statistik Posyandu {self.posyandu_id} - {self.tanggal_statistik}"


class DashboardData(models.Model):
    """Model untuk data dashboard."""
    
    # Data posyandu
    posyandu_id = models.IntegerField()  # ID posyandu
    tanggal_data = models.DateField()
    
    # Data dashboard
    data_dashboard = models.JSONField(
        help_text="Data dashboard dalam format JSON"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-tanggal_data']
        indexes = [
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_data']),
        ]
        unique_together = ['posyandu_id', 'tanggal_data']
    
    def __str__(self):
        return f"Dashboard Data Posyandu {self.posyandu_id} - {self.tanggal_data}"


class ExportLog(models.Model):
    """Model untuk log export laporan."""
    
    # Data export
    laporan = models.ForeignKey(
        Laporan,
        on_delete=models.CASCADE,
        related_name='export_logs'
    )
    
    # Format export
    format_export = models.CharField(
        max_length=20,
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV'),
            ('json', 'JSON'),
        ]
    )
    
    # File export
    file_export = models.FileField(
        upload_to='exports/',
        help_text="File hasil export"
    )
    
    # Status export
    status = models.CharField(
        max_length=20,
        choices=[
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='processing'
    )
    
    # Error message
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Pesan error jika export gagal"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['laporan']),
            models.Index(fields=['status']),
            models.Index(fields=['format_export']),
        ]
    
    def __str__(self):
        return f"Export {self.laporan.nama_laporan} - {self.format_export}"
