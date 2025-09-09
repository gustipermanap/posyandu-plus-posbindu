"""
URLs untuk referral-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReferralViewSet

router = DefaultRouter()
router.register(r'referral', ReferralViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
