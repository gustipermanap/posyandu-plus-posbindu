"""
URLs untuk laporan-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TemplateLaporanViewSet, LaporanViewSet, StatistikPosyanduViewSet,
    DashboardDataViewSet, ExportLogViewSet
)

router = DefaultRouter()
router.register(r'template', TemplateLaporanViewSet)
router.register(r'laporan', LaporanViewSet)
router.register(r'statistik', StatistikPosyanduViewSet)
router.register(r'dashboard', DashboardDataViewSet)
router.register(r'export-log', ExportLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
