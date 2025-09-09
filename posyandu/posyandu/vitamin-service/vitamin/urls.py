"""
URLs untuk vitamin-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JenisVitaminViewSet, PemberianVitaminViewSet, PMTViewSet,
    StokVitaminViewSet, StokPMTViewSet
)

router = DefaultRouter()
router.register(r'jenis', JenisVitaminViewSet)
router.register(r'pemberian', PemberianVitaminViewSet)
router.register(r'pmt', PMTViewSet)
router.register(r'stok-vitamin', StokVitaminViewSet)
router.register(r'stok-pmt', StokPMTViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
