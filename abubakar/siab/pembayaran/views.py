from django.shortcuts import render
from .models import Tagihan, Pembayaran

def lihat_tagihan(request):
    siswa = request.user.siswa
    tagihan = Tagihan.objects.filter(siswa=siswa)
    return render(request, 'pembayaran/tagihan.html', {'tagihan': tagihan})
