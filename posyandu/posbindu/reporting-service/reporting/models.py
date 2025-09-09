"""
Model untuk reporting-service.
Menangani laporan dan statistik POS BINDU PTM.
"""
from django.db import models


class ReportLog(models.Model):
    """Model untuk log laporan yang dibuat."""
    
    # Jenis laporan
    JENIS_LAPORAN_CHOICES = [
        ('harian', 'Laporan Harian'),
        ('mingguan', 'Laporan Mingguan'),
        ('bulanan', 'Laporan Bulanan'),
        ('tahunan', 'Laporan Tahunan'),
        ('khusus', 'Laporan Khusus'),
    ]
    
    # Status laporan
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    nama_laporan = models.CharField(max_length=200)
    jenis_laporan = models.CharField(
        max_length=20,
        choices=JENIS_LAPORAN_CHOICES
    )
    
    # Periode laporan
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField()
    
    # Data laporan
    data_laporan = models.JSONField(
        help_text="Data laporan dalam format JSON"
    )
    
    # File laporan
    file_laporan = models.FileField(
        upload_to='reports/',
        blank=True,
        null=True,
        help_text="File laporan (PDF, Excel, dll)"
    )
    
    # Status laporan
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['jenis_laporan']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_mulai']),
            models.Index(fields=['tanggal_akhir']),
        ]
    
    def __str__(self):
        return f"{self.nama_laporan} - {self.tanggal_mulai} s/d {self.tanggal_akhir}"


class ActivityLog(models.Model):
    """Model untuk log aktivitas sistem."""
    
    # Jenis aktivitas
    JENIS_AKTIVITAS_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    # Modul yang terlibat
    MODUL_CHOICES = [
        ('participant', 'Participant'),
        ('screening', 'Screening'),
        ('examination', 'Examination'),
        ('lab', 'Lab'),
        ('risk_assessment', 'Risk Assessment'),
        ('intervention', 'Intervention'),
        ('referral', 'Referral'),
        ('reporting', 'Reporting'),
    ]
    
    user_id = models.IntegerField()  # ID dari auth service
    modul = models.CharField(
        max_length=20,
        choices=MODUL_CHOICES
    )
    jenis_aktivitas = models.CharField(
        max_length=20,
        choices=JENIS_AKTIVITAS_CHOICES
    )
    
    # Detail aktivitas
    deskripsi = models.TextField()
    data_sebelum = models.JSONField(
        blank=True,
        null=True,
        help_text="Data sebelum perubahan"
    )
    data_sesudah = models.JSONField(
        blank=True,
        null=True,
        help_text="Data sesudah perubahan"
    )
    
    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['modul']),
            models.Index(fields=['jenis_aktivitas']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_aktivitas_display()} - {self.get_modul_display()} - {self.created_at}"


class DashboardData(models.Model):
    """Model untuk data dashboard."""
    
    # Data dashboard
    data_dashboard = models.JSONField(
        help_text="Data dashboard dalam format JSON"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Dashboard Data - {self.created_at}"
