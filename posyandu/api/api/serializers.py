from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posyandu, Anak, Penimbangan

class PosyanduSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posyandu
        fields = '__all__'

class AnakSerializer(serializers.ModelSerializer):
    posyandu_nama = serializers.ReadOnlyField(source='posyandu.nama') # Tambahkan untuk menampilkan nama posyandu
    class Meta:
        model = Anak
        fields = '__all__'

class PenimbanganSerializer(serializers.ModelSerializer):
    pemeriksa = serializers.SlugRelatedField(read_only=True, slug_field='username')
    anak_nama = serializers.ReadOnlyField(source='anak.nama') # Tambahkan untuk menampilkan nama anak
    class Meta:
        model = Penimbangan
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
