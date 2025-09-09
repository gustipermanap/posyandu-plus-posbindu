"""
URLs untuk posyandu-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PosyanduViewSet

router = DefaultRouter()
router.register(r'posyandu', PosyanduViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
