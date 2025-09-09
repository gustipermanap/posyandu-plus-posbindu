"""
Model untuk examination-service.
Menangani pemeriksaan fisik peserta POS BINDU PTM.
"""
from django.db import models
from decimal import Decimal


class VitalSigns(models.Model):
    """Model untuk tanda vital."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Tekanan Darah (2x pengukuran)
    td_sistol_1 = models.IntegerField(help_text="Tekanan darah sistolik pengukuran 1")
    td_diastol_1 = models.IntegerField(help_text="Tekanan darah diastolik pengukuran 1")
    td_sistol_2 = models.IntegerField(help_text="Tekanan darah sistolik pengukuran 2")
    td_diastol_2 = models.IntegerField(help_text="Tekanan darah diastolik pengukuran 2")
    
    # Rerata tekanan darah
    td_sistol_rerata = models.IntegerField(help_text="Rerata tekanan darah sistolik")
    td_diastol_rerata = models.IntegerField(help_text="Rerata tekanan darah diastolik")
    
    # Nadi
    nadi = models.IntegerField(help_text="Denyut nadi per menit")
    
    # Suhu (opsional)
    suhu = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Suhu tubuh dalam Celcius"
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
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Vital Signs Visit {self.visit_id} - {self.td_sistol_rerata}/{self.td_diastol_rerata}"
    
    def calculate_average_bp(self):
        """Menghitung rerata tekanan darah."""
        self.td_sistol_rerata = (self.td_sistol_1 + self.td_sistol_2) // 2
        self.td_diastol_rerata = (self.td_diastol_1 + self.td_diastol_2) // 2
        self.save()
        return self.td_sistol_rerata, self.td_diastol_rerata
    
    def get_bp_category(self):
        """Mengategorikan tekanan darah."""
        if self.td_sistol_rerata < 120 and self.td_diastol_rerata < 80:
            return 'Normal'
        elif self.td_sistol_rerata < 130 and self.td_diastol_rerata < 80:
            return 'Elevated'
        elif self.td_sistol_rerata < 140 or self.td_diastol_rerata < 90:
            return 'High Stage 1'
        elif self.td_sistol_rerata < 180 or self.td_diastol_rerata < 120:
            return 'High Stage 2'
        else:
            return 'Crisis'


class Anthropometry(models.Model):
    """Model untuk antropometri."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Tinggi badan
    tinggi_cm = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Tinggi badan dalam cm"
    )
    
    # Berat badan
    berat_kg = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Berat badan dalam kg"
    )
    
    # IMT (dihitung otomatis)
    imt = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Indeks Massa Tubuh"
    )
    
    # Lingkar perut
    lingkar_perut_cm = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Lingkar perut dalam cm"
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
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Anthropometry Visit {self.visit_id} - IMT: {self.imt}"
    
    def calculate_imt(self):
        """Menghitung IMT."""
        if self.tinggi_cm and self.berat_kg:
            tinggi_m = self.tinggi_cm / 100
            self.imt = self.berat_kg / (tinggi_m ** 2)
            self.save()
            return self.imt
        return None
    
    def get_imt_category(self):
        """Mengategorikan IMT."""
        if self.imt < 18.5:
            return 'Kurus'
        elif self.imt < 25:
            return 'Normal'
        elif self.imt < 30:
            return 'Overweight'
        else:
            return 'Obesitas'
    
    def get_waist_risk(self, jenis_kelamin):
        """Menentukan risiko berdasarkan lingkar perut."""
        if jenis_kelamin == 'Laki-laki':
            if self.lingkar_perut_cm >= 90:
                return 'Risiko Tinggi'
            else:
                return 'Normal'
        else:  # Perempuan
            if self.lingkar_perut_cm >= 80:
                return 'Risiko Tinggi'
            else:
                return 'Normal'


class AdditionalExamination(models.Model):
    """Model untuk pemeriksaan tambahan."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Saturasi O2
    spo2 = models.IntegerField(
        null=True,
        blank=True,
        help_text="Saturasi oksigen dalam %"
    )
    
    # CO test untuk perokok
    co_test = models.IntegerField(
        null=True,
        blank=True,
        help_text="Hasil CO test dalam ppm"
    )
    
    # Pemeriksaan lain
    pemeriksaan_lain = models.TextField(
        blank=True,
        null=True,
        help_text="Pemeriksaan tambahan lainnya"
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
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Additional Exam Visit {self.visit_id} - SpO2: {self.spo2}%"
    
    def get_spo2_category(self):
        """Mengategorikan saturasi oksigen."""
        if self.spo2 is None:
            return 'Tidak Diukur'
        elif self.spo2 >= 95:
            return 'Normal'
        elif self.spo2 >= 90:
            return 'Hipoksia Ringan'
        else:
            return 'Hipoksia Berat'
