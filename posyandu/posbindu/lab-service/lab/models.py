"""
Model untuk lab-service.
Menangani pemeriksaan laboratorium sederhana POS BINDU PTM.
"""
from django.db import models
from decimal import Decimal


class LabExamination(models.Model):
    """Model untuk pemeriksaan laboratorium."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Jenis pemeriksaan
    JENIS_PEMERIKSAAN_CHOICES = [
        ('gdp', 'Gula Darah Puasa'),
        ('gds', 'Gula Darah Sewaktu'),
        ('kol_total', 'Kolesterol Total'),
        ('hdl', 'HDL'),
        ('ldl', 'LDL'),
        ('trigliserida', 'Trigliserida'),
        ('asam_urat', 'Asam Urat'),
    ]
    
    jenis_pemeriksaan = models.CharField(
        max_length=20,
        choices=JENIS_PEMERIKSAAN_CHOICES
    )
    
    # Hasil pemeriksaan
    nilai = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Nilai hasil pemeriksaan"
    )
    
    satuan = models.CharField(
        max_length=10,
        default='mg/dL',
        help_text="Satuan hasil pemeriksaan"
    )
    
    # Data alat dan strip
    alat = models.CharField(
        max_length=100,
        help_text="Nama alat yang digunakan"
    )
    
    lot_strip = models.CharField(
        max_length=50,
        help_text="Nomor lot strip"
    )
    
    exp_strip = models.DateField(
        help_text="Tanggal kedaluwarsa strip"
    )
    
    # Waktu pengambilan
    waktu_ambil = models.DateTimeField(
        help_text="Waktu pengambilan sampel"
    )
    
    # Status puasa (untuk GDP)
    status_puasa = models.BooleanField(
        default=False,
        help_text="Status puasa (untuk GDP)"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan pemeriksaan"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['visit_id']),
            models.Index(fields=['participant_id']),
            models.Index(fields=['jenis_pemeriksaan']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_pemeriksaan_display()} - {self.nilai} {self.satuan}"
    
    def get_interpretation(self):
        """Menginterpretasikan hasil pemeriksaan."""
        if self.jenis_pemeriksaan == 'gdp':
            return self._interpret_gdp()
        elif self.jenis_pemeriksaan == 'gds':
            return self._interpret_gds()
        elif self.jenis_pemeriksaan == 'kol_total':
            return self._interpret_kolesterol()
        elif self.jenis_pemeriksaan == 'hdl':
            return self._interpret_hdl()
        elif self.jenis_pemeriksaan == 'ldl':
            return self._interpret_ldl()
        elif self.jenis_pemeriksaan == 'trigliserida':
            return self._interpret_trigliserida()
        elif self.jenis_pemeriksaan == 'asam_urat':
            return self._interpret_asam_urat()
        return 'Tidak ada interpretasi'
    
    def _interpret_gdp(self):
        """Interpretasi Gula Darah Puasa."""
        if self.nilai < 100:
            return 'Normal'
        elif self.nilai < 126:
            return 'Pra-Diabetes'
        else:
            return 'Diabetes'
    
    def _interpret_gds(self):
        """Interpretasi Gula Darah Sewaktu."""
        if self.nilai < 140:
            return 'Normal'
        elif self.nilai < 200:
            return 'Pra-Diabetes'
        else:
            return 'Diabetes'
    
    def _interpret_kolesterol(self):
        """Interpretasi Kolesterol Total."""
        if self.nilai < 200:
            return 'Normal'
        elif self.nilai < 240:
            return 'Batas Tinggi'
        else:
            return 'Tinggi'
    
    def _interpret_hdl(self):
        """Interpretasi HDL."""
        if self.nilai >= 60:
            return 'Normal'
        elif self.nilai >= 40:
            return 'Batas Rendah'
        else:
            return 'Rendah'
    
    def _interpret_ldl(self):
        """Interpretasi LDL."""
        if self.nilai < 100:
            return 'Normal'
        elif self.nilai < 130:
            return 'Batas Tinggi'
        elif self.nilai < 160:
            return 'Tinggi'
        else:
            return 'Sangat Tinggi'
    
    def _interpret_trigliserida(self):
        """Interpretasi Trigliserida."""
        if self.nilai < 150:
            return 'Normal'
        elif self.nilai < 200:
            return 'Batas Tinggi'
        else:
            return 'Tinggi'
    
    def _interpret_asam_urat(self):
        """Interpretasi Asam Urat."""
        if self.nilai < 7.0:
            return 'Normal'
        else:
            return 'Tinggi'


class StockStrip(models.Model):
    """Model untuk stok strip."""
    
    jenis_pemeriksaan = models.CharField(
        max_length=20,
        choices=LabExamination.JENIS_PEMERIKSAAN_CHOICES
    )
    
    nama_strip = models.CharField(
        max_length=100,
        help_text="Nama strip"
    )
    
    lot_number = models.CharField(
        max_length=50,
        help_text="Nomor lot"
    )
    
    exp_date = models.DateField(
        help_text="Tanggal kedaluwarsa"
    )
    
    jumlah_awal = models.IntegerField(
        help_text="Jumlah strip awal"
    )
    
    jumlah_tersisa = models.IntegerField(
        help_text="Jumlah strip tersisa"
    )
    
    harga_per_strip = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Harga per strip"
    )
    
    supplier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama supplier"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['jenis_pemeriksaan']),
            models.Index(fields=['exp_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.nama_strip} - Lot: {self.lot_number}"
    
    @property
    def is_expired(self):
        """Cek apakah strip sudah kedaluwarsa."""
        from datetime import date
        return self.exp_date < date.today()
    
    @property
    def is_expiring_soon(self):
        """Cek apakah strip akan kedaluwarsa dalam 30 hari."""
        from datetime import date, timedelta
        return self.exp_date <= date.today() + timedelta(days=30)
    
    def use_strip(self, jumlah=1):
        """Mengurangi jumlah strip yang tersisa."""
        if self.jumlah_tersisa >= jumlah:
            self.jumlah_tersisa -= jumlah
            self.save()
            return True
        return False
