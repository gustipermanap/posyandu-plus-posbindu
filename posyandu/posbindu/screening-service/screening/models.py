"""
Model untuk screening-service.
Menangani anamnesis dan kuesioner faktor risiko PTM.
"""
from django.db import models


class Anamnesis(models.Model):
    """Model untuk anamnesis peserta."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Faktor Risiko Merokok
    merokok_status = models.CharField(
        max_length=20,
        choices=[
            ('Tidak', 'Tidak'),
            ('Aktif', 'Aktif'),
            ('Eks', 'Eks'),
        ],
        default='Tidak'
    )
    rokok_batang_per_hari = models.IntegerField(null=True, blank=True)
    
    # Faktor Risiko Alkohol
    alkohol_frekuensi = models.CharField(
        max_length=20,
        choices=[
            ('Tidak', 'Tidak'),
            ('Ya', 'Ya'),
        ],
        default='Tidak'
    )
    alkohol_frekuensi_per_minggu = models.IntegerField(null=True, blank=True)
    
    # Aktivitas Fisik
    aktivitas_menit_per_minggu = models.IntegerField(
        help_text="Total menit aktivitas fisik per minggu"
    )
    jenis_aktivitas = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Jenis aktivitas fisik yang dilakukan"
    )
    
    # Pola Makan
    porsi_sayur_buah_per_hari = models.IntegerField(
        help_text="Jumlah porsi sayur dan buah per hari"
    )
    garam_tinggi = models.BooleanField(
        default=False,
        help_text="Konsumsi garam tinggi"
    )
    gula_tinggi = models.BooleanField(
        default=False,
        help_text="Konsumsi gula tinggi"
    )
    lemak_tinggi = models.BooleanField(
        default=False,
        help_text="Konsumsi lemak tinggi"
    )
    
    # Tidur dan Stres
    tidur_jam = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Jam tidur per hari"
    )
    stres_skala = models.IntegerField(
        choices=[
            (1, 'Sangat Rendah'),
            (2, 'Rendah'),
            (3, 'Sedang'),
            (4, 'Tinggi'),
            (5, 'Sangat Tinggi'),
        ],
        help_text="Skala stres (1-5)"
    )
    
    # Obat Rutin
    obat_rutin = models.JSONField(
        default=list,
        help_text="Daftar obat rutin yang dikonsumsi"
    )
    
    # Kehamilan (untuk perempuan usia subur)
    kehamilan = models.BooleanField(
        default=False,
        help_text="Sedang hamil"
    )
    usia_kehamilan_minggu = models.IntegerField(
        null=True,
        blank=True,
        help_text="Usia kehamilan dalam minggu"
    )
    
    # Alergi dan Kontraindikasi
    alergi = models.TextField(
        blank=True,
        null=True,
        help_text="Riwayat alergi"
    )
    kontraindikasi = models.TextField(
        blank=True,
        null=True,
        help_text="Kontraindikasi untuk pemeriksaan"
    )
    
    # Keluhan dan Gejala
    keluhan_pusing = models.BooleanField(default=False)
    keluhan_nyeri_dada = models.BooleanField(default=False)
    keluhan_sesak = models.BooleanField(default=False)
    keluhan_poliuria = models.BooleanField(default=False)
    keluhan_polidipsia = models.BooleanField(default=False)
    keluhan_bengkak_kaki = models.BooleanField(default=False)
    keluhan_lainnya = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['visit_id']),
            models.Index(fields=['participant_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Anamnesis Visit {self.visit_id} - {self.created_at}"


class RiskFactorScore(models.Model):
    """Model untuk skor faktor risiko."""
    anamnesis = models.OneToOneField(Anamnesis, on_delete=models.CASCADE, related_name='risk_score')
    
    # Skor Merokok (0-3)
    skor_merokok = models.IntegerField(default=0)
    
    # Skor Alkohol (0-2)
    skor_alkohol = models.IntegerField(default=0)
    
    # Skor Aktivitas Fisik (0-2)
    skor_aktivitas = models.IntegerField(default=0)
    
    # Skor Pola Makan (0-3)
    skor_pola_makan = models.IntegerField(default=0)
    
    # Skor Tidur (0-2)
    skor_tidur = models.IntegerField(default=0)
    
    # Skor Stres (0-2)
    skor_stres = models.IntegerField(default=0)
    
    # Total Skor
    total_skor = models.IntegerField(default=0)
    
    # Kategori Risiko
    kategori_risiko = models.CharField(
        max_length=20,
        choices=[
            ('Rendah', 'Rendah'),
            ('Sedang', 'Sedang'),
            ('Tinggi', 'Tinggi'),
        ],
        default='Rendah'
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Risk Score {self.anamnesis.visit_id} - {self.kategori_risiko}"
    
    def calculate_total_score(self):
        """Menghitung total skor faktor risiko."""
        self.total_skor = (
            self.skor_merokok + 
            self.skor_alkohol + 
            self.skor_aktivitas + 
            self.skor_pola_makan + 
            self.skor_tidur + 
            self.skor_stres
        )
        
        # Kategorisasi berdasarkan total skor
        if self.total_skor <= 3:
            self.kategori_risiko = 'Rendah'
        elif self.total_skor <= 6:
            self.kategori_risiko = 'Sedang'
        else:
            self.kategori_risiko = 'Tinggi'
        
        self.save()
        return self.total_skor
