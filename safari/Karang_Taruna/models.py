from django.db import models

class Lomba(models.Model):
    nama_lomba = models.CharField(max_length=255)
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama_lomba

    class Meta:
        verbose_name = 'Lomba'
        verbose_name_plural = 'Lomba'
        ordering = ['nama_lomba']  # Urutkan berdasarkan nama lomba secara default

class Anggota(models.Model):
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nomor_telepon = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'Anggota'
        verbose_name_plural = 'Anggota'
        ordering = ['nama']  # Urutkan berdasarkan nama anggota secara default

class Ketua(models.Model):
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nomor_telepon = models.CharField(max_length=15)
    lomba = models.ForeignKey(Lomba, related_name='ketua_lomba', on_delete=models.CASCADE)
    anggota = models.ManyToManyField(Anggota, blank=True, related_name='peserta_lombas')  # Referensi ke model Anggota yang benar

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = 'Ketua'
        verbose_name_plural = 'Ketua'
        ordering = ['nama']  # Urutkan berdasarkan nama ketua secara default
