"""
URLs untuk risk-assessment-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RiskAssessmentViewSet

router = DefaultRouter()
router.register(r'assessment', RiskAssessmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
