
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PosyanduViewSet, AnakViewSet, PenimbanganViewSet, UserViewSet

router = DefaultRouter()
router.register(r'posyandu', PosyanduViewSet)
router.register(r'anak', AnakViewSet)
router.register(r'penimbangan', PenimbanganViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
