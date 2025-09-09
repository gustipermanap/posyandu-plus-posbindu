from django.contrib import admin
from .models import Murid, Pegawai, RiwayatPekerjaan


class RiwayatPekerjaanInLine(admin.TabularInline):
    model = RiwayatPekerjaan
    extra = 1  # Menambahkan dua form kosong untuk menambah riwayat pekerjaan

class PegawaiAdmin(admin.ModelAdmin):
    inlines = [RiwayatPekerjaanInLine]  # Tambahkan kedua inline di sini
    class Meta:
        model = Pegawai
    

# Register your models here.
admin.site.register(Murid)
admin.site.register(Pegawai, PegawaiAdmin)  # Mendaftarkan PegawaiAdmin
