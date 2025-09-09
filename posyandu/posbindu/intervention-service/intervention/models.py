"""
Model untuk intervention-service.
Menangani edukasi dan intervensi POS BINDU PTM.
"""
from django.db import models


class Intervention(models.Model):
    """Model untuk intervensi dan edukasi."""
    
    # Data kunjungan
    visit_id = models.IntegerField()  # ID dari participant service
    participant_id = models.IntegerField()  # ID dari participant service
    
    # Jenis intervensi
    JENIS_INTERVENSI_CHOICES = [
        ('edukasi', 'Edukasi'),
        ('konseling', 'Konseling'),
        ('monitoring', 'Monitoring'),
        ('rujukan', 'Rujukan'),
    ]
    
    jenis_intervensi = models.CharField(
        max_length=20,
        choices=JENIS_INTERVENSI_CHOICES
    )
    
    # Topik edukasi
    TOPIK_EDUKASI_CHOICES = [
        ('berhenti_merokok', 'Berhenti Merokok'),
        ('diet_ggl', 'Diet GGL (Gula, Garam, Lemak)'),
        ('aktivitas_fisik', 'Aktivitas Fisik'),
        ('kepatuhan_obat', 'Kepatuhan Obat'),
        ('tidur_stres', 'Tidur dan Stres'),
        ('kontrol_berat_badan', 'Kontrol Berat Badan'),
        ('kontrol_td', 'Kontrol Tekanan Darah'),
        ('kontrol_gula_darah', 'Kontrol Gula Darah'),
        ('kontrol_kolesterol', 'Kontrol Kolesterol'),
    ]
    
    topik_edukasi = models.CharField(
        max_length=30,
        choices=TOPIK_EDUKASI_CHOICES,
        blank=True,
        null=True
    )
    
    # Materi edukasi
    materi_edukasi = models.TextField(
        blank=True,
        null=True,
        help_text="Materi edukasi yang diberikan"
    )
    
    # Link materi
    link_materi = models.URLField(
        blank=True,
        null=True,
        help_text="Link ke materi edukasi"
    )
    
    # File materi
    file_materi = models.FileField(
        upload_to='intervention_materials/',
        blank=True,
        null=True,
        help_text="File materi edukasi"
    )
    
    # Catatan konseling
    catatan_konseling = models.TextField(
        blank=True,
        null=True,
        help_text="Catatan konseling yang diberikan"
    )
    
    # Target SMART
    target_spesifik = models.TextField(
        blank=True,
        null=True,
        help_text="Target spesifik yang ditetapkan"
    )
    
    target_terukur = models.TextField(
        blank=True,
        null=True,
        help_text="Target terukur yang ditetapkan"
    )
    
    target_tercapai = models.TextField(
        blank=True,
        null=True,
        help_text="Target tercapai yang ditetapkan"
    )
    
    target_relevan = models.TextField(
        blank=True,
        null=True,
        help_text="Target relevan yang ditetapkan"
    )
    
    target_waktu = models.TextField(
        blank=True,
        null=True,
        help_text="Target waktu yang ditetapkan"
    )
    
    # Status intervensi
    status_intervensi = models.CharField(
        max_length=20,
        choices=[
            ('direncanakan', 'Direncanakan'),
            ('dilaksanakan', 'Dilaksanakan'),
            ('selesai', 'Selesai'),
            ('ditunda', 'Ditunda'),
        ],
        default='direncanakan'
    )
    
    # Tanggal target
    tanggal_target = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal target pencapaian"
    )
    
    # Tanggal evaluasi
    tanggal_evaluasi = models.DateField(
        blank=True,
        null=True,
        help_text="Tanggal evaluasi pencapaian"
    )
    
    # Hasil evaluasi
    hasil_evaluasi = models.TextField(
        blank=True,
        null=True,
        help_text="Hasil evaluasi pencapaian target"
    )
    
    # Skor pencapaian (1-10)
    skor_pencapaian = models.IntegerField(
        blank=True,
        null=True,
        help_text="Skor pencapaian target (1-10)"
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
            models.Index(fields=['jenis_intervensi']),
            models.Index(fields=['topik_edukasi']),
            models.Index(fields=['status_intervensi']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Intervention {self.get_jenis_intervensi_display()} - {self.participant_id}"


class EducationMaterial(models.Model):
    """Model untuk materi edukasi."""
    
    # Informasi materi
    judul = models.CharField(max_length=200, help_text="Judul materi edukasi")
    
    topik = models.CharField(
        max_length=30,
        choices=Intervention.TOPIK_EDUKASI_CHOICES
    )
    
    deskripsi = models.TextField(
        blank=True,
        null=True,
        help_text="Deskripsi materi"
    )
    
    # Konten materi
    konten = models.TextField(
        blank=True,
        null=True,
        help_text="Konten materi edukasi"
    )
    
    # File materi
    file_materi = models.FileField(
        upload_to='education_materials/',
        blank=True,
        null=True,
        help_text="File materi edukasi"
    )
    
    # Link eksternal
    link_eksternal = models.URLField(
        blank=True,
        null=True,
        help_text="Link ke materi eksternal"
    )
    
    # Kategori
    KATEGORI_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('infografis', 'Infografis'),
        ('brosur', 'Brosur'),
        ('link', 'Link Eksternal'),
    ]
    
    kategori = models.CharField(
        max_length=20,
        choices=KATEGORI_CHOICES,
        default='pdf'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
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
            models.Index(fields=['topik']),
            models.Index(fields=['kategori']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.judul} - {self.get_topik_display()}"


class FollowUp(models.Model):
    """Model untuk follow-up intervensi."""
    
    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )
    
    # Tanggal follow-up
    tanggal_follow_up = models.DateField()
    
    # Metode follow-up
    METODE_CHOICES = [
        ('telepon', 'Telepon'),
        ('whatsapp', 'WhatsApp'),
        ('kunjungan', 'Kunjungan'),
        ('online', 'Online'),
    ]
    
    metode_follow_up = models.CharField(
        max_length=20,
        choices=METODE_CHOICES
    )
    
    # Hasil follow-up
    hasil_follow_up = models.TextField(
        help_text="Hasil follow-up"
    )
    
    # Status pencapaian target
    status_pencapaian = models.CharField(
        max_length=20,
        choices=[
            ('belum_dicapai', 'Belum Dicapai'),
            ('sebagian_dicapai', 'Sebagian Dicapai'),
            ('dicapai', 'Dicapai'),
            ('melebihi_target', 'Melebihi Target'),
        ]
    )
    
    # Hambatan
    hambatan = models.TextField(
        blank=True,
        null=True,
        help_text="Hambatan yang ditemui"
    )
    
    # Rencana selanjutnya
    rencana_selanjutnya = models.TextField(
        blank=True,
        null=True,
        help_text="Rencana selanjutnya"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField()  # ID dari auth service
    
    class Meta:
        ordering = ['-tanggal_follow_up']
        indexes = [
            models.Index(fields=['intervention']),
            models.Index(fields=['tanggal_follow_up']),
            models.Index(fields=['metode_follow_up']),
            models.Index(fields=['status_pencapaian']),
        ]
    
    def __str__(self):
        return f"Follow-up {self.intervention} - {self.tanggal_follow_up}"
