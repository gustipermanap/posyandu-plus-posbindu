"""
Views untuk API aplikasi Posyandu.

Modul ini mendefinisikan ViewSet untuk model Posyandu, Anak, Penimbangan, dan User,
bersama dengan logika khusus untuk operasi seperti unggah foto profil.
"""
from django.contrib.auth.models import User # Dipindahkan ke sini untuk pengurutan yang benar
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action # Import action decorator
from rest_framework.response import Response # Import Response
from .models import Posyandu, Anak, Penimbangan, UserProfile # Import UserProfile
from .serializers import PosyanduSerializer, AnakSerializer, \
    PenimbanganSerializer, UserSerializer, PasswordChangeSerializer # Import all Serializers

# Create your views here.

class PosyanduViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """API endpoint yang memungkinkan data Posyandu untuk dilihat atau diedit."""
    queryset = Posyandu.objects.all() # pylint: disable=no-member
    serializer_class = PosyanduSerializer
    permission_classes = [IsAuthenticated]

class AnakViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """API endpoint yang memungkinkan data Anak untuk dilihat atau diedit."""
    queryset = Anak.objects.all() # pylint: disable=no-member
    serializer_class = AnakSerializer
    permission_classes = [IsAuthenticated]

class PenimbanganViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """API endpoint yang memungkinkan data Penimbangan untuk dilihat atau diedit."""
    queryset = Penimbangan.objects.all() # pylint: disable=no-member
    serializer_class = PenimbanganSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Menyimpan objek Penimbangan baru dan mengaitkannya dengan user yang melakukan request."""
        serializer.save(pemeriksa=self.request.user)

    def perform_update(self, serializer):
        """Memperbarui objek Penimbangan yang ada dan mengaitkannya dengan user 
yang melakukan request."""
        serializer.save(pemeriksa=self.request.user)

class UserViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """API endpoint yang memungkinkan data User untuk dilihat atau diedit."""
    queryset = User.objects.all() # pylint: disable=no-member
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['patch'],
        url_path='upload-profile-picture'
    )
    def upload_profile_picture(self, request, pk=None): # pylint: disable=unused-argument
        """Mengunggah atau memperbarui foto profil untuk User."""
        print(f"DEBUG: request.user in upload_profile_picture: {request.user}") # Debug print
        user = self.get_object()
        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist: # pylint: disable=no-member
            user_profile = UserProfile.objects.create(user=user) # pylint: disable=no-member

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()
            return Response({'detail': 'Foto profil berhasil diunggah.'},
                            status=status.HTTP_200_OK) # pylint: disable=line-too-long
        return Response({'detail': 'Tidak ada foto yang diunggah.'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='set-password')
    def set_password(self, request, pk=None): # pylint: disable=unused-argument
        """Mengatur kata sandi baru untuk pengguna."""
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.data.get('old_password')):
            return Response({'old_password': ['Kata sandi lama salah.']},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({'detail': 'Kata sandi berhasil diatur ulang.'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='server-time')
    def server_time(self, request): # pylint: disable=unused-argument
        """Mengembalikan waktu server saat ini."""
        current_time = timezone.now()
        return Response({'server_time': current_time.isoformat()},
                        status=status.HTTP_200_OK)
