from django.db import models
from kurikulum_merdeka.models import Siswa

class Tagihan(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    keterangan = models.CharField(max_length=255)
    tanggal_dibuat = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.siswa.nama} - {self.jumlah}"

class Pembayaran(models.Model):
    tagihan = models.ForeignKey(Tagihan, on_delete=models.CASCADE)
    jumlah_dibayar = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal_bayar = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pembayaran {self.tagihan.siswa.nama} - {self.jumlah_dibayar}"
