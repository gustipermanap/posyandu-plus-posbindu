"""
URLs untuk participant-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ParticipantViewSet, VisitViewSet, LocationViewSet, UserInfoView

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/user-info/', UserInfoView.as_view(), name='user_info'),
]
