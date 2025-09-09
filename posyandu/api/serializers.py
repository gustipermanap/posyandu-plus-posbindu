"""
Serializers untuk API aplikasi Posyandu.

Modul ini mendefinisikan serializer untuk model Posyandu, Anak, Penimbangan, dan User,
yang mengubah objek model menjadi format JSON dan sebaliknya untuk operasi API.
"""
from django.contrib.auth.models import User # Diperlukan untuk UserSerializer
from rest_framework import serializers
from .models import Posyandu, Anak, Penimbangan

class PosyanduSerializer(serializers.ModelSerializer):
    """Serializer untuk model Posyandu."""
    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = Posyandu
        fields = '__all__'

class AnakSerializer(serializers.ModelSerializer):
    """Serializer untuk model Anak."""
    posyandu_nama = serializers.ReadOnlyField(source='posyandu.nama')
    posyandu = serializers.PrimaryKeyRelatedField(queryset=Posyandu.objects.all(), required=True)
    
    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = Anak
        fields = [
            'id', 'nama', 'nik_anak', 'nama_bapak', 'no_hp_bapak', 'nama_ibu', 
            'no_hp_ibu', 'tanggal_lahir', 'jenis_kelamin', 'posyandu', 'posyandu_nama'
        ]
    
    def validate_posyandu(self, value):
        """Validasi bahwa posyandu yang dipilih valid."""
        if not value:
            raise serializers.ValidationError("Posyandu harus dipilih.")
        return value

class PenimbanganSerializer(serializers.ModelSerializer):
    """Serializer untuk model Penimbangan."""
    pemeriksa = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = Penimbangan
        fields = '__all__' # Ensure waktu_penimbangan is included here

class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk model User, termasuk foto profil."""
    profile_picture = serializers.SerializerMethodField() # Add this line

    class Meta: # pylint: disable=missing-class-docstring, too-few-public-methods
        model = User
        fields = ('id', 'username', 'profile_picture') # Add 'profile_picture' here

    def get_profile_picture(self, obj):
        """Mengembalikan URL absolut untuk foto profil pengguna."""
        if obj.userprofile.profile_picture:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.userprofile.profile_picture.url)
            return obj.userprofile.profile_picture.url
        return None

class PasswordChangeSerializer(serializers.Serializer):
    """Serializer untuk mengubah kata sandi pengguna."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
