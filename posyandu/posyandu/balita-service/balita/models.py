"""
Model untuk balita-service.
Menangani pemeriksaan balita POS BINDU PTM.
"""
from django.db import models
from decimal import Decimal


class PemeriksaanBalita(models.Model):
    """Model untuk pemeriksaan balita."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    balita_id = models.IntegerField()  # ID balita
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal pemeriksaan
    tanggal_pemeriksaan = models.DateField()
    
    # Antropometri
    berat_badan = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Berat badan dalam kg"
    )
    tinggi_badan = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Tinggi badan dalam cm"
    )
    lingkar_kepala = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Lingkar kepala dalam cm"
    )
    lingkar_lengan = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Lingkar lengan atas dalam cm"
    )
    
    # Status gizi (dihitung otomatis)
    status_gizi = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'Normal'),
            ('kurang', 'Gizi Kurang'),
            ('buruk', 'Gizi Buruk'),
            ('lebih', 'Gizi Lebih'),
            ('obesitas', 'Obesitas'),
        ],
        blank=True,
        null=True
    )
    
    # Perkembangan anak
    motorik_kasar = models.CharField(
        max_length=20,
        choices=[
            ('sesuai', 'Sesuai'),
            ('meragukan', 'Meragukan'),
            ('menyimpang', 'Menyimpang'),
        ],
        default='sesuai'
    )
    
    motorik_halus = models.CharField(
        max_length=20,
        choices=[
            ('sesuai', 'Sesuai'),
            ('meragukan', 'Meragukan'),
            ('menyimpang', 'Menyimpang'),
        ],
        default='sesuai'
    )
    
    bicara = models.CharField(
        max_length=20,
        choices=[
            ('sesuai', 'Sesuai'),
            ('meragukan', 'Meragukan'),
            ('menyimpang', 'Menyimpang'),
        ],
        default='sesuai'
    )
    
    sosial = models.CharField(
        max_length=20,
        choices=[
            ('sesuai', 'Sesuai'),
            ('meragukan', 'Meragukan'),
            ('menyimpang', 'Menyimpang'),
        ],
        default='sesuai'
    )
    
    # Catatan perkembangan
    catatan_perkembangan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan perkembangan anak"
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi untuk orang tua"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_pemeriksaan']
        indexes = [
            models.Index(fields=['visit_id']),
            models.Index(fields=['balita_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_pemeriksaan']),
        ]
    
    def __str__(self):
        return f"Pemeriksaan Balita {self.balita_id} - {self.tanggal_pemeriksaan}"
    
    def calculate_status_gizi(self, umur_bulan, jenis_kelamin):
        """Menghitung status gizi berdasarkan BB/TB dan umur."""
        # Implementasi sederhana - dalam implementasi nyata gunakan chart WHO
        if umur_bulan < 24:
            # Untuk balita < 2 tahun, gunakan BB/TB
            if self.berat_badan < 7.0:
                return 'buruk'
            elif self.berat_badan < 8.5:
                return 'kurang'
            elif self.berat_badan > 12.0:
                return 'lebih'
            else:
                return 'normal'
        else:
            # Untuk balita 2-5 tahun, gunakan IMT
            if self.tinggi_badan > 0:
                imt = self.berat_badan / ((self.tinggi_badan / 100) ** 2)
                if imt < 14.0:
                    return 'buruk'
                elif imt < 16.0:
                    return 'kurang'
                elif imt > 20.0:
                    return 'obesitas'
                else:
                    return 'normal'
        return 'normal'


class ImunisasiBalita(models.Model):
    """Model untuk imunisasi balita."""
    
    # Data balita
    balita_id = models.IntegerField()  # ID balita
    posyandu_id = models.IntegerField()  # ID posyandu
    
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
        choices=JENIS_IMUNISASI_CHOICES
    )
    
    # Tanggal imunisasi
    tanggal_imunisasi = models.DateField()
    
    # Usia saat imunisasi (dalam bulan)
    usia_saat_imunisasi = models.IntegerField()
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('diberikan', 'Diberikan'),
            ('tidak_diberikan', 'Tidak Diberikan'),
            ('kontraindikasi', 'Kontraindikasi'),
        ],
        default='diberikan'
    )
    
    # Alasan tidak diberikan
    alasan_tidak_diberikan = models.TextField(
        blank=True,
        null=True,
        help_text="Alasan jika tidak diberikan"
    )
    
    # Lokasi imunisasi
    lokasi_imunisasi = models.CharField(
        max_length=100,
        choices=[
            ('posyandu', 'Posyandu'),
            ('puskesmas', 'Puskesmas'),
            ('rumah_sakit', 'Rumah Sakit'),
            ('klinik', 'Klinik'),
        ],
        default='posyandu'
    )
    
    # Petugas
    petugas_imunisasi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nama petugas yang memberikan imunisasi"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan imunisasi"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_imunisasi']
        indexes = [
            models.Index(fields=['balita_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_imunisasi']),
            models.Index(fields=['tanggal_imunisasi']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_imunisasi_display()} - {self.balita_id}"


class VitaminBalita(models.Model):
    """Model untuk pemberian vitamin balita."""
    
    # Data balita
    balita_id = models.IntegerField()  # ID balita
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Jenis vitamin
    JENIS_VITAMIN_CHOICES = [
        ('vitamin_a', 'Vitamin A'),
        ('vitamin_d', 'Vitamin D'),
        ('pmt', 'PMT (Pemberian Makanan Tambahan)'),
    ]
    
    jenis_vitamin = models.CharField(
        max_length=20,
        choices=JENIS_VITAMIN_CHOICES
    )
    
    # Tanggal pemberian
    tanggal_pemberian = models.DateField()
    
    # Dosis
    dosis = models.CharField(
        max_length=50,
        help_text="Dosis vitamin yang diberikan"
    )
    
    # Status
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
    
    # Petugas
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
            models.Index(fields=['balita_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_vitamin']),
            models.Index(fields=['tanggal_pemberian']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_vitamin_display()} - {self.balita_id}"
