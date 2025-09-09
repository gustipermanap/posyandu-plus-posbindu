from django.db import models
from django.contrib.auth.models import User

class Murid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nis = models.CharField(max_length=20)
    alamat = models.TextField()
    tanggal_lahir = models.DateField()
    nama_ayah = models.CharField(max_length=100)
    email_ayah = models.EmailField()
    no_tlp_ayah = models.CharField(max_length=15)
    nama_ibu = models.CharField(max_length=100)
    email_ibu = models.EmailField()
    no_tlp_ibu = models.CharField(max_length=15)

class Anak(models.Model):
    nama = models.CharField(max_length=30)
    def __str__(self):
       return self.nama 

class Pegawai(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    nip = models.CharField(max_length=20)
    tanggal_lahir = models.DateField()
    alamat = models.TextField()
    no_telp = models.CharField(max_length=15)
    email = models.EmailField()
    pendidikan_terakhir = models.CharField(max_length=100)
    nama_suami_istri = models.CharField(max_length=100)
    anak = models.ManyToManyField(Anak, related_name='pegawai', blank=True, null=True)  # Relasi ke model Anak
    

class RiwayatPekerjaan(models.Model):
    pegawai = models.ForeignKey(Pegawai, on_delete=models.CASCADE)  # Hubungkan dengan DetailKeluarga
    nama_perusahaan = models.CharField(max_length=100)
    posisi = models.CharField(max_length=100)
    tahun_masa_kerja = models.CharField(max_length=50) 
