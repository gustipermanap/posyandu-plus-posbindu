from django.shortcuts import render
from django.http import  HttpResponse
from .models import RW, Organisasi, Struktur, Acara, Fasilitas, Tentang, About, rt1, rt2, rt3, rt4, rt5, rt6, rt7, rt8, rt9, rt10, rt11

def home(request):
    slide = RW.objects.all()
    blog = Organisasi.objects.all()[0:6]
#    blog = Blog.objects.all()
    acara = Acara.objects.all()[0:6]
    fasilitas = Fasilitas.objects.all()
    about = About.objects.all()
    context = {
        'slide': slide,
        'blog': blog,
        'acara': acara,
        'fasilitas': fasilitas,
        'about': about,
        }    
    return render(
        request, 'beranda.html', context)

def blog(request, slug):
    daftar = Organisasi.objects.get(slug=slug)
    
    return render(request, 'list_blog.html', {'daftar': daftar})

def event(request):
    acara = Acara.objects.all()
    context = {
        'acara': acara,
        } 
    return render(request, 'event.html', context)

def tentang(request):
    about = About.objects.filter()
    tentang = Tentang.objects.all()
    pengurus = Struktur.objects.all()
    context = {
        'about': about,
        'tentang': tentang,
        'pengurus': pengurus,
    }
    return render(request, 'tentang-kami.html', context)

def fasiltias(request):
    fasilitas = Fasilitas.objects.all()
    return render(request, 'fasilitas.html', {'fasilitas': fasilitas,})

def contact(request):
    return render(request, 'kontak.html')

def listacara(request, slug):
    acara = Acara.objects.get(slug=slug)
    return render(request, 'list_acara.html', {'acara': acara})

def satu(request):
    RT = rt1.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt1.html', context)

def dua(request):
    RT = rt2.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt2.html', context)

def tiga(request):
    RT = rt3.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt3.html', context)

def empat(request):
    RT = rt4.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt4.html', context)

def lima(request):
    RT = rt5.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt5.html', context)

def enam(request):
    RT = rt6.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt6.html', context)

def tujuh(request):
    RT = rt7.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt7.html', context)

def delapan(request):
    RT = rt8.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt8.html', context)

def sembilan(request):
    RT = rt9.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt9.html', context)

def sepuluh(request):
    RT = rt10.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt10.html', context)

def sebelas(request):
    RT = rt11.objects.all()
    context = {
        'RT': RT,
    }
    return render(request, 'rt11.html', context)









