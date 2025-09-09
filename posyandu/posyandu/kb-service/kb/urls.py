"""
URLs untuk kb-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MetodeKBViewSet, PencatatanKBViewSet, KonselingKBViewSet,
    StokKBViewSet, RujukanKBViewSet
)

router = DefaultRouter()
router.register(r'metode', MetodeKBViewSet)
router.register(r'pencatatan', PencatatanKBViewSet)
router.register(r'konseling', KonselingKBViewSet)
router.register(r'stok', StokKBViewSet)
router.register(r'rujukan', RujukanKBViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
