"""
Model untuk auth-service.
Hanya menangani User dan UserProfile.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Model untuk menyimpan informasi profil tambahan untuk pengguna Django."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Hubungan satu-ke-satu dengan model User bawaan Django"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Gambar profil pengguna (opsional)"
    )

    def __str__(self):
        """Mengembalikan representasi string dari objek UserProfile."""
        return self.user.username
