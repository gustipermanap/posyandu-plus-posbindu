"""
Serializers untuk auth-service.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk model User."""
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = ['id']
    
    def get_profile_picture(self, obj):
        """Mengambil URL gambar profil pengguna."""
        try:
            profile = obj.userprofile
            if profile.profile_picture:
                return profile.profile_picture.url
        except UserProfile.DoesNotExist:
            pass
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer untuk model UserProfile."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'profile_picture']
        read_only_fields = ['id', 'user']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer untuk registrasi pengguna baru."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        """Validasi password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password tidak cocok.")
        return attrs
    
    def create(self, validated_data):
        """Membuat user baru."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user
