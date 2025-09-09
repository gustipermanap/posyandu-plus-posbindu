from django.urls import path
from . import views

urlpatterns = [
    path('rapor/', views.lihat_rapor, name='lihat_rapor'),
]
