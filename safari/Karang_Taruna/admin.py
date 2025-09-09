from django.contrib import admin
from .models import Lomba, Ketua, Anggota

class AnggotaInline(admin.TabularInline):
    model = Ketua.anggota.through  # Relasi Many-to-Many antara Ketua dan Anggota
    extra = 1  # Menambahkan baris kosong untuk input anggota baru

class KetuaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'nomor_telepon', 'lomba')
    search_fields = ('nama', 'email', 'nomor_telepon')
    list_filter = ('lomba',)
    inlines = [AnggotaInline]  # Menampilkan form untuk anggota dalam halaman Ketua

class LombaAdmin(admin.ModelAdmin):
    list_display = ('nama_lomba',)
    search_fields = ('nama_lomba',)

class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'nomor_telepon')
    search_fields = ('nama', 'email', 'nomor_telepon')

admin.site.register(Lomba, LombaAdmin)
admin.site.register(Ketua, KetuaAdmin)
admin.site.register(Anggota, AnggotaAdmin)
