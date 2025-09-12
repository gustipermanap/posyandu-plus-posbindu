"""
Model untuk ibu-hamil-service.
Menangani pemeriksaan ibu hamil POS BINDU PTM.
"""
from django.db import models
from decimal import Decimal


class PemeriksaanIbuHamil(models.Model):
    """Model untuk pemeriksaan ibu hamil."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    ibu_hamil_id = models.IntegerField()  # ID ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal pemeriksaan
    tanggal_pemeriksaan = models.DateField()
    
    # Usia kehamilan
    usia_kehamilan_minggu = models.IntegerField(help_text="Usia kehamilan dalam minggu")
    
    # Pemeriksaan fisik
    tekanan_darah_sistol = models.IntegerField(help_text="Tekanan darah sistolik")
    tekanan_darah_diastol = models.IntegerField(help_text="Tekanan darah diastolik")
    nadi = models.IntegerField(help_text="Denyut nadi per menit")
    
    # Pemeriksaan kehamilan
    tinggi_fundus = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Tinggi fundus dalam cm"
    )
    lingkar_lengan_atas = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Lingkar lengan atas dalam cm"
    )
    gerakan_janin = models.BooleanField(
        default=True,
        help_text="Gerakan janin terasa"
    )
    
    # Pemeriksaan laboratorium
    hb = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Kadar hemoglobin dalam g/dL"
    )
    protein_urine = models.CharField(
        max_length=20,
        choices=[
            ('negatif', 'Negatif'),
            ('positif', 'Positif'),
            ('+1', '+1'),
            ('+2', '+2'),
            ('+3', '+3'),
        ],
        default='negatif'
    )
    gula_darah = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Gula darah dalam mg/dL"
    )
    
    # Keluhan
    keluhan = models.TextField(
        blank=True,
        null=True,
        help_text="Keluhan yang dirasakan"
    )
    
    # Risiko kehamilan
    risiko_tinggi = models.BooleanField(default=False)
    jenis_risiko = models.TextField(
        blank=True,
        null=True,
        help_text="Jenis risiko kehamilan"
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi untuk ibu hamil"
    )
    
    # Rujukan
    perlu_rujukan = models.BooleanField(default=False)
    alasan_rujukan = models.TextField(
        blank=True,
        null=True,
        help_text="Alasan rujukan"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_pemeriksaan']
        indexes = [
            models.Index(fields=['visit_id']),
            models.Index(fields=['ibu_hamil_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_pemeriksaan']),
        ]
    
    def __str__(self):
        return f"Pemeriksaan Ibu Hamil {self.ibu_hamil_id} - {self.tanggal_pemeriksaan}"
    
    def check_risiko_tinggi(self):
        """Mengecek apakah termasuk risiko tinggi."""
        risiko = []
        
        # Tekanan darah tinggi
        if self.tekanan_darah_sistol >= 140 or self.tekanan_darah_diastol >= 90:
            risiko.append("Hipertensi")
        
        # Anemia
        if self.hb and self.hb < 11.0:
            risiko.append("Anemia")
        
        # Protein urine positif
        if self.protein_urine in ['positif', '+1', '+2', '+3']:
            risiko.append("Proteinuria")
        
        # Gula darah tinggi
        if self.gula_darah and self.gula_darah >= 140:
            risiko.append("Diabetes Gestasional")
        
        # LILA rendah
        if self.lingkar_lengan_atas < 23.5:
            risiko.append("Kurang Energi Kronis")
        
        if risiko:
            self.risiko_tinggi = True
            self.jenis_risiko = ", ".join(risiko)
        else:
            self.risiko_tinggi = False
            self.jenis_risiko = ""
        
        self.save()
        return self.risiko_tinggi


class SuplemenIbuHamil(models.Model):
    """Model untuk pemberian suplemen ibu hamil."""
    
    # Data ibu hamil
    ibu_hamil_id = models.IntegerField()  # ID ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Jenis suplemen
    JENIS_SUPLEMEN_CHOICES = [
        ('fe_tablet', 'Fe Tablet'),
        ('kalsium', 'Kalsium'),
        ('asam_folat', 'Asam Folat'),
        ('vitamin_d', 'Vitamin D'),
    ]
    
    jenis_suplemen = models.CharField(
        max_length=20,
        choices=JENIS_SUPLEMEN_CHOICES
    )
    
    # Tanggal pemberian
    tanggal_pemberian = models.DateField()
    
    # Dosis
    dosis = models.CharField(
        max_length=50,
        help_text="Dosis suplemen yang diberikan"
    )
    
    # Jumlah
    jumlah = models.IntegerField(help_text="Jumlah suplemen yang diberikan")
    
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
        help_text="Nama petugas yang memberikan suplemen"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan pemberian suplemen"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_pemberian']
        indexes = [
            models.Index(fields=['ibu_hamil_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['jenis_suplemen']),
            models.Index(fields=['tanggal_pemberian']),
        ]
    
    def __str__(self):
        return f"{self.get_jenis_suplemen_display()} - {self.ibu_hamil_id}"


class IbuNifas(models.Model):
    """Model untuk data ibu nifas."""
    
    # Data ibu
    ibu_hamil_id = models.IntegerField()  # ID ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal persalinan
    tanggal_persalinan = models.DateField()
    
    # Jenis persalinan
    jenis_persalinan = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'Normal'),
            ('sectio', 'Sectio Caesarea'),
            ('forceps', 'Forceps'),
            ('vakum', 'Vakum'),
        ]
    )
    
    # Tempat persalinan
    tempat_persalinan = models.CharField(
        max_length=50,
        choices=[
            ('rumah_sakit', 'Rumah Sakit'),
            ('puskesmas', 'Puskesmas'),
            ('klinik', 'Klinik'),
            ('rumah', 'Rumah'),
        ]
    )
    
    # Kondisi ibu
    kondisi_ibu = models.CharField(
        max_length=20,
        choices=[
            ('baik', 'Baik'),
            ('kurang_baik', 'Kurang Baik'),
            ('buruk', 'Buruk'),
        ],
        default='baik'
    )
    
    # Keluhan
    keluhan = models.TextField(
        blank=True,
        null=True,
        help_text="Keluhan yang dirasakan"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('nifas', 'Nifas'),
            ('selesai', 'Selesai'),
        ],
        default='nifas'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_persalinan']
        indexes = [
            models.Index(fields=['ibu_hamil_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_persalinan']),
        ]
    
    def __str__(self):
        return f"Ibu Nifas {self.ibu_hamil_id} - {self.tanggal_persalinan}"


class BayiBaruLahir(models.Model):
    """Model untuk data bayi baru lahir."""
    
    # Data ibu
    ibu_hamil_id = models.IntegerField()  # ID ibu hamil
    posyandu_id = models.IntegerField()  # ID posyandu
    
    # Tanggal lahir
    tanggal_lahir = models.DateField()
    jam_lahir = models.TimeField()
    
    # Jenis kelamin
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ]
    )
    
    # Berat lahir
    berat_lahir = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Berat lahir dalam kg"
    )
    
    # Panjang lahir
    panjang_lahir = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Panjang lahir dalam cm"
    )
    
    # Lingkar kepala
    lingkar_kepala = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Lingkar kepala dalam cm"
    )
    
    # Kondisi lahir
    kondisi_lahir = models.CharField(
        max_length=20,
        choices=[
            ('baik', 'Baik'),
            ('kurang_baik', 'Kurang Baik'),
            ('buruk', 'Buruk'),
        ],
        default='baik'
    )
    
    # APGAR Score
    apgar_1 = models.IntegerField(
        null=True,
        blank=True,
        help_text="APGAR Score 1 menit"
    )
    apgar_5 = models.IntegerField(
        null=True,
        blank=True,
        help_text="APGAR Score 5 menit"
    )
    
    # IMD (Inisiasi Menyusu Dini)
    imd = models.BooleanField(
        default=False,
        help_text="Inisiasi Menyusu Dini"
    )
    
    # Imunisasi HB0
    imunisasi_hb0 = models.BooleanField(
        default=False,
        help_text="Imunisasi HB0"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('hidup', 'Hidup'),
            ('meninggal', 'Meninggal'),
        ],
        default='hidup'
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
        ordering = ['-tanggal_lahir']
        indexes = [
            models.Index(fields=['ibu_hamil_id']),
            models.Index(fields=['posyandu_id']),
            models.Index(fields=['tanggal_lahir']),
        ]
    
    def __str__(self):
        return f"Bayi Baru Lahir {self.ibu_hamil_id} - {self.tanggal_lahir}"
