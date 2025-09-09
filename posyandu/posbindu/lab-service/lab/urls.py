"""
URLs untuk lab-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabResultViewSet, StockViewSet

router = DefaultRouter()
router.register(r'result', LabResultViewSet)
router.register(r'stock', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
