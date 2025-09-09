"""
Definisi model-model Django untuk aplikasi Posyandu.

Model-model ini mencakup entitas utama seperti Posyandu, Anak, Penimbangan, dan Profil Pengguna.
Setiap model mendefinisikan struktur data dan hubungan antar data dalam database.
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posyandu(models.Model):
    """Model untuk merepresentasikan data Posyandu."""
    nama = models.CharField(max_length=100)
    alamat = models.TextField()

    def __str__(self):
        """Mengembalikan representasi string dari objek Posyandu."""
        return self.nama # pylint: disable=invalid-str-returned

class Anak(models.Model):
    """Model untuk merepresentasikan data Anak."""
    nama = models.CharField(max_length=100)
    nik_anak = models.CharField(
        max_length=16, 
        blank=True, 
        null=True, 
        help_text="Nomor Induk Kependudukan Anak (opsional)"
    )
    nama_bapak = models.CharField(max_length=100, blank=True, null=True)
    no_hp_bapak = models.CharField(max_length=15, blank=True, null=True)
    nama_ibu = models.CharField(max_length=100, blank=True, null=True)
    no_hp_ibu = models.CharField(max_length=15, blank=True, null=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[
            ('Laki-laki', 'Laki-laki'),
            ('Perempuan', 'Perempuan')
        ],
        help_text="Jenis kelamin anak"
    )
    posyandu = models.ForeignKey(
        Posyandu,
        on_delete=models.CASCADE,
        help_text="Posyandu tempat anak terdaftar"
    )

    def __str__(self):
        """Mengembalikan representasi string dari objek Anak."""
        return self.nama # pylint: disable=invalid-str-returned

class Penimbangan(models.Model):
    """Model untuk merepresentasikan data Penimbangan Anak."""
    anak = models.ForeignKey(
        Anak,
        on_delete=models.CASCADE,
        help_text="Anak yang ditimbang"
    )
    tanggal_penimbangan = models.DateField(
        help_text="Tanggal penimbangan dilakukan"
    )
    waktu_penimbangan = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Waktu pencatatan penimbangan"
    )
    berat_badan = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Berat badan anak dalam kg"
    )
    tinggi_badan = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Tinggi badan anak dalam cm"
    )
    lingkar_kepala = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Lingkar kepala anak dalam cm"
    )
    lingkar_lengan_atas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Lingkar lengan atas anak dalam cm"
    )
    catatan_khusus = models.TextField(
        null=True,
        blank=True,
        help_text="Catatan khusus dari petugas"
    )
    status_gizi = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Status gizi anak (Normal, Kurang, Lebih, dll)"
    )
    keterangan = models.TextField(
        null=True,
        blank=True,
        help_text="Keterangan tambahan"
    )
    foto_penimbangan = models.ImageField(
        upload_to='penimbangan_photos/',
        null=True,
        blank=True,
        help_text="Foto dokumentasi penimbangan"
    )
    tempat_penimbangan = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Tempat penimbangan dilakukan"
    )
    pemeriksa = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Pengguna yang melakukan penimbangan (opsional)"
    )

    def __str__(self):
        """Mengembalikan representasi string dari objek Penimbangan."""
        return f"{self.anak.nama} - {self.tanggal_penimbangan}" # pylint: disable=no-member

class UserProfile(models.Model):
    """Model untuk menyimpan informasi profil tambahan untuk pengguna Django."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Hubungan satu-ke-satu dengan model User bawaan Django"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Gambar profil pengguna (opsional)"
    )

    def __str__(self):
        """Mengembalikan representasi string dari objek UserProfile."""
        return self.user.username # pylint: disable=no-member
