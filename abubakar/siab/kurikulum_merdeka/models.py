from django.db import models
from django.contrib.auth.models import User

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    NAMA_CHOICES = [
        ('banin', 'Banin'),
        ('banat', 'Banat'),
    ]
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=10)
    jenis_kelamin = models.CharField(max_length=5, choices=NAMA_CHOICES)
    tanggal_lahir = models.DateField()

    def __str__(self):
        return self.nama

class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    mata_pelajaran = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama

class Nilai(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    nilai_angka = models.DecimalField(max_digits=5, decimal_places=2)
    nilai_huruf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.siswa} - {self.mata_pelajaran} - {self.nilai_angka}"
