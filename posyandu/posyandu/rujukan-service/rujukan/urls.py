"""
URLs untuk rujukan-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FasilitasKesehatanViewSet, RujukanViewSet, FollowUpRujukanViewSet,
    TemplateRujukanViewSet
)

router = DefaultRouter()
router.register(r'fasilitas', FasilitasKesehatanViewSet)
router.register(r'rujukan', RujukanViewSet)
router.register(r'follow-up', FollowUpRujukanViewSet)
router.register(r'template', TemplateRujukanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
