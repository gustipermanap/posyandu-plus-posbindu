"""
Views untuk auth-service.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """View untuk registrasi pengguna baru."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View untuk melihat dan mengupdate profil pengguna."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Mengambil profil pengguna yang sedang login."""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Mengembalikan informasi pengguna yang sedang login."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_picture(request):
    """Mengupdate gambar profil pengguna."""
    try:
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Profil tidak ditemukan'}, 
            status=status.HTTP_404_NOT_FOUND
        )
