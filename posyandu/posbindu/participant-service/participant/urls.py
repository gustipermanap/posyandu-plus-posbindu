"""
URLs untuk participant-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, VisitViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
