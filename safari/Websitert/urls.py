from django.contrib import admin
# from Websitert import views
from django.urls import path, include
from Websitert import views

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.home, name='home'),
    path('about/', views.tentang, name='tentang-kami'),
    path('RT1/', views.satu, name='rt1'),
    path('RT2/', views.dua, name='rt2'),
    path('RT3/', views.tiga, name='rt3'),
    path('RT4/', views.empat, name='rt4'),
    path('RT5/', views.lima, name='rt5'),
    path('RT6/', views.enam, name='rt6'),
    path('RT7/', views.tujuh, name='rt7'),
    path('RT8/', views.delapan, name='rt8'),
    path('RT9/', views.sembilan, name='rt9'),
    path('RT10/', views.sepuluh, name='rt10'),
    path('RT11/', views.sebelas, name='rt11'),
    path('acara<slug>/', views.listacara, name='list-acara'),
    path('<slug>/', views.blog, name ='blog'),
]



