"""
Model untuk vitamin-service.
Menangani vitamin & PMT.
"""
from django.db import models
from decimal import Decimal


class JenisVitamin(models.Model):
    """Model untuk jenis vitamin yang tersedia."""
    
    # Jenis vitamin
    JENIS_VITAMIN_CHOICES = [
        ('vitamin_a', 'Vitamin A'),
        ('vitamin_d', 'Vitamin D'),
        ('vitamin_e', 'Vitamin E'),
        ('vitamin_k', 'Vitamin K'),
        ('vitamin_b1', 'Vitamin B1 (Tiamin)'),
        ('vitamin_b2', 'Vitamin B2 (Riboflavin)'),
        ('vitamin_b3', 'Vitamin B3 (Niasin)'),
        ('vitamin_b6', 'Vitamin B6 (Piridoksin)'),
        ('vitamin_b12', 'Vitamin B12 (Kobalamin)'),
        ('asam_folat', 'Asam Folat'),
        ('vitamin_c', 'Vitamin C'),
        ('kalsium', 'Kalsium'),
        ('zat_besi', 'Zat Besi'),
        ('seng', 'Seng (Zinc)'),
        ('yodium', 'Yodium'),
    ]
    
    jenis_vitamin = models.CharField(
        max_length=20,
        choices=JENIS_VITAMIN_CHOICES,
        unique=True
    )
    
    # Deskripsi vitamin
    deskripsi = models.TextField(
        blank=True,
        null=True,
        help_text="Deskripsi vitamin"
    )
    
    # Dosis harian yang dianjurkan
    dosis_harian_anak = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dosis harian untuk anak (mg/mcg)"
    )
    
    dosis_harian_dewasa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dosis harian untuk dewasa (mg/mcg)"
    )
    
    # Unit dosis
    unit_dosis = models.CharField(
        max_length=10,
        choices=[
            ('mg', 'mg'),
            ('mcg', 'mcg'),
            ('IU', 'IU'),
            ('g', 'g'),
        ],
        default='mg'
    )
    
    # Indikasi
    indikasi = models.TextField(
        blank=True,
        null=True,
        help_text="Indikasi pemberian vitamin"
    )
    
    # Kontraindikasi
    kontraindikasi = models.TextField(
        blank=True,
        null=True,
        help_text="Kontraindikasi vitamin"
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
        ordering = ['jenis_vitamin']
        indexes = [
            models.Index(fields=['jenis_vitamin']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return self.get_jenis_vitamin_display()


class PemberianVitamin(models.Model):
    """Model untuk pemberian vitamin."""
    
    # Data penerima
    penerima_id = models.IntegerField()  # ID balita atau ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    jenis_penerima = models.CharField(
        max_length=20,
        choices=[
            ('balita', 'Balita'),
            ('ibu_hamil', 'Ibu Hamil'),
            ('wus', 'WUS'),
        ]
    )
    
    # Jenis vitamin
    jenis_vitamin = models.CharField(
        max_length=20,
        choices=JenisVitamin.JENIS_VITAMIN_CHOICES
    )
    
    # Tanggal pemberian
    tanggal_pemberian = models.DateField()
    
    # Dosis yang diberikan
    dosis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Dosis yang diberikan"
    )
    
    # Unit dosis
    unit_dosis = models.CharField(
        max_length=10,
        choices=[
            ('mg', 'mg'),
            ('mcg', 'mcg'),
            ('IU', 'IU'),
            ('g', 'g'),
        ],
        default='mg'
    )
    
    # Status pemberian
    status = models.CharField(
        max_length=20,
        choices=[
            ('diberikan', 'Diberikan'),
            ('tidak_diberikan', 'Tidak Diberikan'),
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
    
    # Petugas pemberian
    petugas_pemberian = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang memberikan vitamin"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan pemberian vitamin"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_pemberian']
        indexes = [
            models.Index(fields=['penerima_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_penerima']),
            models.Index(fields=['jenis_vitamin']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_pemberian']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_vitamin_display()} - {self.penerima_id} - {self.tanggal_pemberian}"


class PMT(models.Model):
    """Model untuk Pemberian Makanan Tambahan (PMT)."""
    
    # Data penerima
    penerima_id = models.IntegerField()  # ID balita atau ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    jenis_penerima = models.CharField(
        max_length=20,
        choices=[
            ('balita', 'Balita'),
            ('ibu_hamil', 'Ibu Hamil'),
            ('wus', 'WUS'),
        ]
    )
    
    # Jenis PMT
    jenis_pmt = models.CharField(
        max_length=50,
        choices=[
            ('biskuit', 'Biskuit PMT'),
            ('susu', 'Susu PMT'),
            ('bubur', 'Bubur PMT'),
            ('kacang_hijau', 'Kacang Hijau'),
            ('telur', 'Telur'),
            ('daging', 'Daging'),
            ('ikan', 'Ikan'),
            ('sayuran', 'Sayuran'),
            ('buah', 'Buah'),
        ]
    )
    
    # Tanggal pemberian
    tanggal_pemberian = models.DateField()
    
    # Jumlah yang diberikan
    jumlah = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Jumlah PMT yang diberikan"
    )
    
    # Unit jumlah
    unit_jumlah = models.CharField(
        max_length=20,
        choices=[
            ('gram', 'gram'),
            ('kg', 'kg'),
            ('pcs', 'pcs'),
            ('bungkus', 'bungkus'),
            ('porsi', 'porsi'),
        ],
        default='gram'
    )
    
    # Status pemberian
    status = models.CharField(
        max_length=20,
        choices=[
            ('diberikan', 'Diberikan'),
            ('tidak_diberikan', 'Tidak Diberikan'),
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
    
    # Petugas pemberian
    petugas_pemberian = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang memberikan PMT"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan pemberian PMT"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_pemberian']
        indexes = [
            models.Index(fields=['penerima_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_penerima']),
            models.Index(fields=['jenis_pmt']),
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_pemberian']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_pmt_display()} - {self.penerima_id} - {self.tanggal_pemberian}"


class StokVitamin(models.Model):
    """Model untuk stok vitamin."""
    
    # Jenis vitamin
    jenis_vitamin = models.CharField(
        max_length=20,
        choices=JenisVitamin.JENIS_VITAMIN_CHOICES
    )
    
    # Nama produk
    nama_produk = models.CharField(
        max_length=100,
        help_text="Nama produk vitamin"
    )
    
    # Batch
    batch_number = models.CharField(
        max_length=50,
        help_text="Nomor batch"
    )
    
    # Tanggal kedaluwarsa
    tanggal_kedaluwarsa = models.DateField()
    
    # Jumlah stok
    jumlah_stok = models.IntegerField(help_text="Jumlah vitamin tersisa")
    
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
            models.Index(fields=['jenis_vitamin']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['tanggal_kedaluwarsa']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.nama_produk} - Batch: {self.batch_number}"
    
    @property
    def is_expired(self):
        """Cek apakah vitamin sudah kedaluwarsa."""
        from datetime import date
        return self.tanggal_kedaluwarsa < date.today()
    
    @property
    def is_expiring_soon(self):
        """Cek apakah vitamin akan kedaluwarsa dalam 30 hari."""
        from datetime import date, timedelta
        return self.tanggal_kedaluwarsa <= date.today() + timedelta(days=30)
    
    def use_vitamin(self, jumlah=1):
        """Mengurangi jumlah stok vitamin."""
        if self.jumlah_stok >= jumlah:
            self.jumlah_stok -= jumlah
            if self.jumlah_stok == 0:
                self.status = 'habis'
            self.save()
            return True
        return False


class StokPMT(models.Model):
    """Model untuk stok PMT."""
    
    # Jenis PMT
    jenis_pmt = models.CharField(
        max_length=50,
        choices=[
            ('biskuit', 'Biskuit PMT'),
            ('susu', 'Susu PMT'),
            ('bubur', 'Bubur PMT'),
            ('kacang_hijau', 'Kacang Hijau'),
            ('telur', 'Telur'),
            ('daging', 'Daging'),
            ('ikan', 'Ikan'),
            ('sayuran', 'Sayuran'),
            ('buah', 'Buah'),
        ]
    )
    
    # Nama produk
    nama_produk = models.CharField(
        max_length=100,
        help_text="Nama produk PMT"
    )
    
    # Batch
    batch_number = models.CharField(
        max_length=50,
        help_text="Nomor batch"
    )
    
    # Tanggal kedaluwarsa
    tanggal_kedaluwarsa = models.DateField()
    
    # Jumlah stok
    jumlah_stok = models.IntegerField(help_text="Jumlah PMT tersisa")
    
    # Unit stok
    unit_stok = models.CharField(
        max_length=20,
        choices=[
            ('gram', 'gram'),
            ('kg', 'kg'),
            ('pcs', 'pcs'),
            ('bungkus', 'bungkus'),
        ],
        default='gram'
    )
    
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
            models.Index(fields=['jenis_pmt']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['tanggal_kedaluwarsa']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.nama_produk} - Batch: {self.batch_number}"
    
    @property
    def is_expired(self):
        """Cek apakah PMT sudah kedaluwarsa."""
        from datetime import date
        return self.tanggal_kedaluwarsa < date.today()
    
    @property
    def is_expiring_soon(self):
        """Cek apakah PMT akan kedaluwarsa dalam 30 hari."""
        from datetime import date, timedelta
        return self.tanggal_kedaluwarsa <= date.today() + timedelta(days=30)
    
    def use_pmt(self, jumlah=1):
        """Mengurangi jumlah stok PMT."""
        if self.jumlah_stok >= jumlah:
            self.jumlah_stok -= jumlah
            if self.jumlah_stok == 0:
                self.status = 'habis'
            self.save()
            return True
        return False
