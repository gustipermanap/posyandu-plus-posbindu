from django.db import models
from django.utils.text import slugify

class KartuKeluarga(models.Model):
#id=models.IntegerField(primary_key=True)
    nomor_KK = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = "Kartu Keluarga"
    def save(self) :
        self.nomor_KK=slugify(self.nomor_KK)
        super(KartuKeluarga, self).save()
        
    def __str__(self):
        return '{}'.format(self.nomor_KK)

class KartuTandaPenduduk(models.Model):
# id=models.IntegerField(primary_key=True)
    nomor_KK = models.ForeignKey(KartuKeluarga, max_length=20, on_delete=models.CASCADE, related_name='Kartukeluarga')
    NIK = models.IntegerField()
    nama = models.CharField(max_length=30)
    alamat = models.CharField(max_length=80)
    tempat_lahir = models.CharField(max_length=20)
    tanggal_lahir = models.DateField()
    telp = models.IntegerField(default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kartu Tanda Penduduk"
    def save(self):
        self.nomor_kk=slugify(self.nama)
        super(KartuTandaPenduduk, self).save()
        
    def __str__(self):
        return '{}'.format(self.nama)


