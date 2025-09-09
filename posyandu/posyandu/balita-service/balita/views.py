"""
Views untuk balita-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import PemeriksaanBalita, ImunisasiBalita, VitaminBalita
from .serializers import (
    PemeriksaanBalitaSerializer, ImunisasiBalitaSerializer, 
    VitaminBalitaSerializer, BalitaSearchSerializer
)


class PemeriksaanBalitaViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PemeriksaanBalita."""
    queryset = PemeriksaanBalita.objects.all()
    serializer_class = PemeriksaanBalitaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balita_id', 'posyandu_id', 'status_gizi', 'tanggal_pemeriksaan']
    search_fields = ['balita_id', 'posyandu_id']
    ordering_fields = ['tanggal_pemeriksaan', 'created_at']
    ordering = ['-tanggal_pemeriksaan']
    
    @action(detail=False, methods=['get'])
    def by_balita(self, request):
        """Mengambil pemeriksaan berdasarkan balita."""
        balita_id = request.query_params.get('balita_id')
        if not balita_id:
            return Response(
                {'error': 'balita_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(balita_id=balita_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_posyandu(self, request):
        """Mengambil pemeriksaan berdasarkan posyandu."""
        posyandu_id = request.query_params.get('posyandu_id')
        if not posyandu_id:
            return Response(
                {'error': 'posyandu_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(posyandu_id=posyandu_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik pemeriksaan balita."""
        total_pemeriksaan = self.queryset.count()
        by_status_gizi = {
            'normal': self.queryset.filter(status_gizi='normal').count(),
            'kurang': self.queryset.filter(status_gizi='kurang').count(),
            'buruk': self.queryset.filter(status_gizi='buruk').count(),
            'lebih': self.queryset.filter(status_gizi='lebih').count(),
        }
        by_perkembangan = {
            'sesuai': self.queryset.filter(
                motorik_kasar='sesuai',
                motorik_halus='sesuai',
                bicara='sesuai',
                sosial='sesuai'
            ).count(),
            'meragukan': self.queryset.filter(
                Q(motorik_kasar='meragukan') | 
                Q(motorik_halus='meragukan') | 
                Q(bicara='meragukan') | 
                Q(sosial='meragukan')
            ).count(),
            'menyimpang': self.queryset.filter(
                Q(motorik_kasar='menyimpang') | 
                Q(motorik_halus='menyimpang') | 
                Q(bicara='menyimpang') | 
                Q(sosial='menyimpang')
            ).count(),
        }
        
        return Response({
            'total_pemeriksaan': total_pemeriksaan,
            'by_status_gizi': by_status_gizi,
            'by_perkembangan': by_perkembangan,
        })


class ImunisasiBalitaViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model ImunisasiBalita."""
    queryset = ImunisasiBalita.objects.all()
    serializer_class = ImunisasiBalitaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balita_id', 'posyandu_id', 'jenis_imunisasi', 'status', 'tanggal_imunisasi']
    search_fields = ['balita_id', 'posyandu_id', 'petugas_imunisasi']
    ordering_fields = ['tanggal_imunisasi', 'created_at']
    ordering = ['-tanggal_imunisasi']
    
    @action(detail=False, methods=['get'])
    def by_balita(self, request):
        """Mengambil imunisasi berdasarkan balita."""
        balita_id = request.query_params.get('balita_id')
        if not balita_id:
            return Response(
                {'error': 'balita_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(balita_id=balita_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil imunisasi berdasarkan jenis."""
        jenis_imunisasi = request.query_params.get('jenis_imunisasi')
        if not jenis_imunisasi:
            return Response(
                {'error': 'jenis_imunisasi parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_imunisasi=jenis_imunisasi)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik imunisasi."""
        total_imunisasi = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'kontraindikasi': self.queryset.filter(status='kontraindikasi').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in ImunisasiBalita.JENIS_IMUNISASI_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_imunisasi=choice[0]).count()
        
        return Response({
            'total_imunisasi': total_imunisasi,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class VitaminBalitaViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model VitaminBalita."""
    queryset = VitaminBalita.objects.all()
    serializer_class = VitaminBalitaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balita_id', 'posyandu_id', 'jenis_vitamin', 'status', 'tanggal_pemberian']
    search_fields = ['balita_id', 'posyandu_id', 'petugas_pemberian']
    ordering_fields = ['tanggal_pemberian', 'created_at']
    ordering = ['-tanggal_pemberian']
    
    @action(detail=False, methods=['get'])
    def by_balita(self, request):
        """Mengambil vitamin berdasarkan balita."""
        balita_id = request.query_params.get('balita_id')
        if not balita_id:
            return Response(
                {'error': 'balita_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(balita_id=balita_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil vitamin berdasarkan jenis."""
        jenis_vitamin = request.query_params.get('jenis_vitamin')
        if not jenis_vitamin:
            return Response(
                {'error': 'jenis_vitamin parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_vitamin=jenis_vitamin)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik vitamin."""
        total_vitamin = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in VitaminBalita.JENIS_VITAMIN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_vitamin=choice[0]).count()
        
        return Response({
            'total_vitamin': total_vitamin,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })
