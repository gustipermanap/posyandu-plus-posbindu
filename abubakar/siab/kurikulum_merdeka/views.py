from django.shortcuts import render
from .models import Siswa, Nilai

def lihat_rapor(request):
    siswa = Siswa.objects.get(user=request.user)
    nilai_siswa = Nilai.objects.filter(siswa=siswa)
    return render(request, 'penilaian/rapor.html', {'nilai_siswa': nilai_siswa})
