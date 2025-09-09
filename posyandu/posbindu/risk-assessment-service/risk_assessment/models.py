"""
Model untuk risk-assessment-service.
Menangani penilaian risiko kardiovaskular POS BINDU PTM.
"""
from django.db import models
from decimal import Decimal
import math


class RiskAssessment(models.Model):
    """Model untuk penilaian risiko kardiovaskular."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Data peserta (untuk perhitungan)
    umur = models.IntegerField(help_text="Umur dalam tahun")
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ]
    )
    
    # Data klinis
    td_sistol = models.IntegerField(help_text="Tekanan darah sistolik")
    td_diastol = models.IntegerField(help_text="Tekanan darah diastolik")
    merokok = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    kolesterol_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Kolesterol total dalam mg/dL"
    )
    hdl = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="HDL dalam mg/dL"
    )
    imt = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Indeks Massa Tubuh"
    )
    lingkar_perut = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Lingkar perut dalam cm"
    )
    
    # Skor risiko
    skor_risiko_cvd = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Skor risiko kardiovaskular 10-tahun"
    )
    
    # Kategori risiko
    kategori_risiko = models.CharField(
        max_length=20,
        choices=[
            ('Rendah', 'Rendah (<5%)'),
            ('Sedang', 'Sedang (5-10%)'),
            ('Tinggi', 'Tinggi (10-20%)'),
            ('Sangat Tinggi', 'Sangat Tinggi (>20%)'),
        ]
    )
    
    # Flag rujukan
    flag_rujukan = models.BooleanField(default=False)
    alasan_rujukan = models.TextField(
        blank=True,
        null=True,
        help_text="Alasan rujukan"
    )
    
    # Rekomendasi
    rekomendasi = models.TextField(
        blank=True,
        null=True,
        help_text="Rekomendasi berdasarkan penilaian risiko"
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
            models.Index(fields=['kategori_risiko']),
            models.Index(fields=['flag_rujukan']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Risk Assessment Visit {self.visit_id} - {self.kategori_risiko}"
    
    def calculate_cvd_risk(self):
        """Menghitung skor risiko kardiovaskular 10-tahun."""
        # Implementasi sederhana berdasarkan faktor risiko
        # Dalam implementasi nyata, gunakan chart WHO/CVD yang lebih akurat
        
        risk_score = 0
        
        # Faktor umur
        if self.umur >= 60:
            risk_score += 3
        elif self.umur >= 50:
            risk_score += 2
        elif self.umur >= 40:
            risk_score += 1
        
        # Faktor jenis kelamin
        if self.jenis_kelamin == 'Laki-laki':
            risk_score += 1
        
        # Faktor tekanan darah
        if self.td_sistol >= 180 or self.td_diastol >= 110:
            risk_score += 4
        elif self.td_sistol >= 160 or self.td_diastol >= 100:
            risk_score += 3
        elif self.td_sistol >= 140 or self.td_diastol >= 90:
            risk_score += 2
        elif self.td_sistol >= 130 or self.td_diastol >= 80:
            risk_score += 1
        
        # Faktor merokok
        if self.merokok:
            risk_score += 2
        
        # Faktor diabetes
        if self.diabetes:
            risk_score += 2
        
        # Faktor kolesterol
        if self.kolesterol_total:
            if self.kolesterol_total >= 240:
                risk_score += 2
            elif self.kolesterol_total >= 200:
                risk_score += 1
        
        # Faktor HDL
        if self.hdl:
            if self.hdl < 40:
                risk_score += 1
        
        # Faktor IMT
        if self.imt:
            if self.imt >= 30:
                risk_score += 2
            elif self.imt >= 25:
                risk_score += 1
        
        # Faktor lingkar perut
        if self.lingkar_perut:
            if self.jenis_kelamin == 'Laki-laki' and self.lingkar_perut >= 90:
                risk_score += 1
            elif self.jenis_kelamin == 'Perempuan' and self.lingkar_perut >= 80:
                risk_score += 1
        
        self.skor_risiko_cvd = risk_score
        
        # Kategorisasi risiko
        if risk_score <= 2:
            self.kategori_risiko = 'Rendah'
        elif risk_score <= 4:
            self.kategori_risiko = 'Sedang'
        elif risk_score <= 6:
            self.kategori_risiko = 'Tinggi'
        else:
            self.kategori_risiko = 'Sangat Tinggi'
        
        # Tentukan flag rujukan
        self._determine_referral_flag()
        
        self.save()
        return risk_score
    
    def _determine_referral_flag(self):
        """Menentukan apakah perlu rujukan."""
        reasons = []
        
        # Kriteria rujukan berdasarkan tekanan darah
        if self.td_sistol >= 180 or self.td_diastol >= 110:
            reasons.append("Tekanan darah krisis")
        
        # Kriteria rujukan berdasarkan skor risiko
        if self.skor_risiko_cvd >= 6:
            reasons.append("Skor risiko tinggi")
        
        # Kriteria rujukan berdasarkan diabetes
        if self.diabetes and self.td_sistol >= 140:
            reasons.append("Diabetes dengan hipertensi")
        
        # Kriteria rujukan berdasarkan kolesterol
        if self.kolesterol_total and self.kolesterol_total >= 240:
            reasons.append("Kolesterol sangat tinggi")
        
        if reasons:
            self.flag_rujukan = True
            self.alasan_rujukan = "; ".join(reasons)
        else:
            self.flag_rujukan = False
            self.alasan_rujukan = ""
    
    def generate_recommendations(self):
        """Membuat rekomendasi berdasarkan penilaian risiko."""
        recommendations = []
        
        # Rekomendasi berdasarkan tekanan darah
        if self.td_sistol >= 140 or self.td_diastol >= 90:
            recommendations.append("Kontrol tekanan darah dengan diet rendah garam dan olahraga teratur")
        
        # Rekomendasi berdasarkan merokok
        if self.merokok:
            recommendations.append("Berhenti merokok untuk mengurangi risiko kardiovaskular")
        
        # Rekomendasi berdasarkan diabetes
        if self.diabetes:
            recommendations.append("Kontrol gula darah dengan diet dan obat sesuai anjuran dokter")
        
        # Rekomendasi berdasarkan kolesterol
        if self.kolesterol_total and self.kolesterol_total >= 200:
            recommendations.append("Diet rendah lemak dan konsultasi untuk pengobatan kolesterol")
        
        # Rekomendasi berdasarkan IMT
        if self.imt and self.imt >= 25:
            recommendations.append("Turunkan berat badan dengan diet seimbang dan olahraga")
        
        # Rekomendasi berdasarkan lingkar perut
        if self.lingkar_perut:
            if self.jenis_kelamin == 'Laki-laki' and self.lingkar_perut >= 90:
                recommendations.append("Kurangi lingkar perut dengan olahraga dan diet")
            elif self.jenis_kelamin == 'Perempuan' and self.lingkar_perut >= 80:
                recommendations.append("Kurangi lingkar perut dengan olahraga dan diet")
        
        # Rekomendasi umum
        if self.kategori_risiko in ['Tinggi', 'Sangat Tinggi']:
            recommendations.append("Konsultasi rutin dengan dokter untuk monitoring")
        
        self.rekomendasi = "; ".join(recommendations)
        self.save()
        return self.rekomendasi
