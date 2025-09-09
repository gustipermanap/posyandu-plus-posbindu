"""
URLs untuk screening-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnamnesisViewSet

router = DefaultRouter()
router.register(r'anamnesis', AnamnesisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
