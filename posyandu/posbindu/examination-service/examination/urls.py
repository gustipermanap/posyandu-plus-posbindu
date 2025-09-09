"""
URLs untuk examination-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VitalSignsViewSet, AnthropometryViewSet

router = DefaultRouter()
router.register(r'vital-signs', VitalSignsViewSet)
router.register(r'anthropometry', AnthropometryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
