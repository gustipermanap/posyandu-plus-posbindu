from django.contrib import admin
from .models import Siswa, Guru, MataPelajaran, Nilai

admin.site.register(Siswa)
admin.site.register(Guru)
admin.site.register(MataPelajaran)
admin.site.register(Nilai)
