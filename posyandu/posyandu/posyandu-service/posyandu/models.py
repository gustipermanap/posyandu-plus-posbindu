"""
Model untuk posyandu-service.
Menangani data Posyandu fokus pada ibu & anak.
"""
from django.db import models
from decimal import Decimal


class Posyandu(models.Model):
    """Model untuk merepresentasikan data Posyandu."""
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True, null=True)
    kabupaten = models.CharField(max_length=100, blank=True, null=True)
    
    # Informasi kader
    nama_koordinator = models.CharField(max_length=100, blank=True, null=True)
    no_hp_koordinator = models.CharField(max_length=15, blank=True, null=True)
    
    # Jadwal kegiatan
    jadwal_posyandu = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Jadwal posyandu (contoh: Setiap hari Selasa minggu ke-2)"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('aktif', 'Aktif'),
            ('tidak_aktif', 'Tidak Aktif'),
        ],
        default='aktif'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Mengembalikan representasi string dari objek Posyandu."""
        return self.nama


class Balita(models.Model):
    """Model untuk data balita (0-59 bulan)."""
    
    # Identitas balita
    nik = models.CharField(
        max_length=16,
        unique=True,
        help_text="NIK balita"
    )
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ]
    )
    
    # Data orang tua/wali
    nama_ayah = models.CharField(max_length=100, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100)
    no_kk = models.CharField(max_length=16, blank=True, null=True)
    no_hp_ortu = models.CharField(max_length=15, blank=True, null=True)
    
    # Alamat
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    
    # Data posyandu
    posyandu = models.ForeignKey(
        Posyandu,
        on_delete=models.CASCADE,
        related_name='balita'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('aktif', 'Aktif'),
            ('tidak_aktif', 'Tidak Aktif'),
            ('pindah', 'Pindah'),
        ],
        default='aktif'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama']
        indexes = [
            models.Index(fields=['nik']),
            models.Index(fields=['posyandu']),
            models.Index(fields=['tanggal_lahir']),
        ]
    
    def __str__(self):
        return f"{self.nama} ({self.nik})"
    
    @property
    def umur_bulan(self):
        """Menghitung umur dalam bulan."""
        from datetime import date
        today = date.today()
        return (today.year - self.tanggal_lahir.year) * 12 + (today.month - self.tanggal_lahir.month)


class IbuHamil(models.Model):
    """Model untuk data ibu hamil."""
    
    # Identitas ibu
    nik = models.CharField(
        max_length=16,
        unique=True,
        help_text="NIK ibu hamil"
    )
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    nama_suami = models.CharField(max_length=100, blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    
    # Alamat
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    
    # Data kehamilan
    hpht = models.DateField(help_text="Hari Pertama Haid Terakhir")
    hpl = models.DateField(help_text="Hari Perkiraan Lahir")
    usia_kehamilan_minggu = models.IntegerField(help_text="Usia kehamilan dalam minggu")
    
    # Riwayat kehamilan
    gravida = models.IntegerField(default=1, help_text="Jumlah kehamilan")
    para = models.IntegerField(default=0, help_text="Jumlah persalinan")
    abortus = models.IntegerField(default=0, help_text="Jumlah keguguran")
    
    # Risiko kehamilan
    risiko_tinggi = models.BooleanField(default=False)
    jenis_risiko = models.TextField(blank=True, null=True, help_text="Jenis risiko kehamilan")
    
    # Rencana persalinan
    rencana_persalinan = models.CharField(
        max_length=50,
        choices=[
            ('RS', 'Rumah Sakit'),
            ('Puskesmas', 'Puskesmas'),
            ('Bidan', 'Bidan'),
            ('Rumah', 'Rumah'),
        ],
        default='RS'
    )
    
    # Data posyandu
    posyandu = models.ForeignKey(
        Posyandu,
        on_delete=models.CASCADE,
        related_name='ibu_hamil'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('hamil', 'Hamil'),
            ('melahirkan', 'Melahirkan'),
            ('nifas', 'Nifas'),
            ('selesai', 'Selesai'),
        ],
        default='hamil'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama']
        indexes = [
            models.Index(fields=['nik']),
            models.Index(fields=['posyandu']),
            models.Index(fields=['hpht']),
        ]
    
    def __str__(self):
        return f"{self.nama} - {self.usia_kehamilan_minggu} minggu"
    
    def calculate_hpl(self):
        """Menghitung HPL dari HPHT."""
        from datetime import timedelta
        self.hpl = self.hpht + timedelta(days=280)
        return self.hpl
    
    def calculate_usia_kehamilan(self):
        """Menghitung usia kehamilan dalam minggu."""
        from datetime import date
        today = date.today()
        diff = today - self.hpht
        self.usia_kehamilan_minggu = diff.days // 7
        return self.usia_kehamilan_minggu


class WUS(models.Model):
    """Model untuk Wanita Usia Subur (WUS)."""
    
    # Identitas
    nik = models.CharField(
        max_length=16,
        unique=True,
        help_text="NIK WUS"
    )
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    nama_suami = models.CharField(max_length=100, blank=True, null=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    
    # Alamat
    alamat = models.TextField()
    rt = models.CharField(max_length=3, blank=True, null=True)
    rw = models.CharField(max_length=3, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    
    # Status KB
    status_kb = models.CharField(
        max_length=20,
        choices=[
            ('aktif', 'Aktif KB'),
            ('tidak_aktif', 'Tidak Aktif KB'),
            ('hamil', 'Sedang Hamil'),
            ('menyusui', 'Menyusui'),
        ],
        default='tidak_aktif'
    )
    
    # Metode KB
    metode_kb = models.CharField(
        max_length=50,
        choices=[
            ('pil', 'Pil KB'),
            ('suntik', 'Suntik KB'),
            ('iud', 'IUD'),
            ('implant', 'Implant'),
            ('kondom', 'Kondom'),
            ('mow', 'MOW'),
            ('mop', 'MOP'),
            ('laktasi', 'Laktasi'),
        ],
        blank=True,
        null=True
    )
    
    # Riwayat kehamilan
    jumlah_anak_hidup = models.IntegerField(default=0)
    jumlah_anak_meninggal = models.IntegerField(default=0)
    
    # Data posyandu
    posyandu = models.ForeignKey(
        Posyandu,
        on_delete=models.CASCADE,
        related_name='wus'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nama']
        indexes = [
            models.Index(fields=['nik']),
            models.Index(fields=['posyandu']),
            models.Index(fields=['status_kb']),
        ]
    
    def __str__(self):
        return f"{self.nama} - {self.get_status_kb_display()}"
