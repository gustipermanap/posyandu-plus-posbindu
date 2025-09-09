"""
URLs untuk imunisasi-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JadwalImunisasiViewSet, PencatatanImunisasiViewSet,
    ReminderImunisasiViewSet, VaksinStockViewSet
)

router = DefaultRouter()
router.register(r'jadwal', JadwalImunisasiViewSet)
router.register(r'pencatatan', PencatatanImunisasiViewSet)
router.register(r'reminder', ReminderImunisasiViewSet)
router.register(r'stok', VaksinStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
