"""
URLs untuk intervention-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterventionViewSet

router = DefaultRouter()
router.register(r'intervention', InterventionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
