"""
URLs untuk balita-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PemeriksaanBalitaViewSet, ImunisasiBalitaViewSet, VitaminBalitaViewSet

router = DefaultRouter()
router.register(r'pemeriksaan', PemeriksaanBalitaViewSet)
router.register(r'imunisasi', ImunisasiBalitaViewSet)
router.register(r'vitamin', VitaminBalitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
