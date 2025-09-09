"""
URLs untuk reporting-service.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportLogViewSet, ActivityLogViewSet, DashboardDataViewSet

router = DefaultRouter()
router.register(r'report-log', ReportLogViewSet)
router.register(r'activity-log', ActivityLogViewSet)
router.register(r'dashboard', DashboardDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
