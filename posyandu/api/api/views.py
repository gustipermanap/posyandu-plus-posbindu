from api.models import Posyandu, Anak, Penimbangan
from .serializers import PosyanduSerializer, AnakSerializer, PenimbanganSerializer, UserSerializer # Import UserSerializer
from django.contrib.auth.models import User # Import User model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PenimbanganViewSet(viewsets.ModelViewSet):
    queryset = Penimbangan.objects.all()
    serializer_class = PenimbanganSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
