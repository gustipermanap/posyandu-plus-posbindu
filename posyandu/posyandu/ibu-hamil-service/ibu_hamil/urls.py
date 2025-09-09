"""
URLs untuk ibu-hamil-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PemeriksaanIbuHamilViewSet, SuplemenIbuHamilViewSet,
    IbuNifasViewSet, BayiBaruLahirViewSet
)

router = DefaultRouter()
router.register(r'pemeriksaan', PemeriksaanIbuHamilViewSet)
router.register(r'suplemen', SuplemenIbuHamilViewSet)
router.register(r'nifas', IbuNifasViewSet)
router.register(r'bayi-baru-lahir', BayiBaruLahirViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
