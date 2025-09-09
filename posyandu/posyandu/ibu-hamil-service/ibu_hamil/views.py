"""
Views untuk ibu-hamil-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import PemeriksaanIbuHamil, SuplemenIbuHamil, IbuNifas, BayiBaruLahir
from .serializers import (
    PemeriksaanIbuHamilSerializer, SuplemenIbuHamilSerializer,
    IbuNifasSerializer, BayiBaruLahirSerializer, IbuHamilSearchSerializer
)


class PemeriksaanIbuHamilViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PemeriksaanIbuHamil."""
    queryset = PemeriksaanIbuHamil.objects.all()
    serializer_class = PemeriksaanIbuHamilSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ibu_hamil_id', 'posyandu_id', 'risiko_tinggi', 'tanggal_pemeriksaan']
    search_fields = ['ibu_hamil_id', 'posyandu_id', 'keluhan']
    ordering_fields = ['tanggal_pemeriksaan', 'created_at']
    ordering = ['-tanggal_pemeriksaan']
    
    @action(detail=False, methods=['get'])
    def by_ibu_hamil(self, request):
        """Mengambil pemeriksaan berdasarkan ibu hamil."""
        ibu_hamil_id = request.query_params.get('ibu_hamil_id')
        if not ibu_hamil_id:
            return Response(
                {'error': 'ibu_hamil_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(ibu_hamil_id=ibu_hamil_id)
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
        """Statistik pemeriksaan ibu hamil."""
        total_pemeriksaan = self.queryset.count()
        by_risiko = {
            'normal': self.queryset.filter(risiko_tinggi=False).count(),
            'tinggi': self.queryset.filter(risiko_tinggi=True).count(),
        }
        by_rujukan = {
            'perlu_rujukan': self.queryset.filter(perlu_rujukan=True).count(),
            'tidak_perlu_rujukan': self.queryset.filter(perlu_rujukan=False).count(),
        }
        
        return Response({
            'total_pemeriksaan': total_pemeriksaan,
            'by_risiko': by_risiko,
            'by_rujukan': by_rujukan,
        })


class SuplemenIbuHamilViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model SuplemenIbuHamil."""
    queryset = SuplemenIbuHamil.objects.all()
    serializer_class = SuplemenIbuHamilSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ibu_hamil_id', 'posyandu_id', 'jenis_suplemen', 'status', 'tanggal_pemberian']
    search_fields = ['ibu_hamil_id', 'posyandu_id', 'petugas_pemberian']
    ordering_fields = ['tanggal_pemberian', 'created_at']
    ordering = ['-tanggal_pemberian']
    
    @action(detail=False, methods=['get'])
    def by_ibu_hamil(self, request):
        """Mengambil suplemen berdasarkan ibu hamil."""
        ibu_hamil_id = request.query_params.get('ibu_hamil_id')
        if not ibu_hamil_id:
            return Response(
                {'error': 'ibu_hamil_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(ibu_hamil_id=ibu_hamil_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil suplemen berdasarkan jenis."""
        jenis_suplemen = request.query_params.get('jenis_suplemen')
        if not jenis_suplemen:
            return Response(
                {'error': 'jenis_suplemen parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_suplemen=jenis_suplemen)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik suplemen."""
        total_suplemen = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in SuplemenIbuHamil.JENIS_SUPLEMEN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_suplemen=choice[0]).count()
        
        return Response({
            'total_suplemen': total_suplemen,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class IbuNifasViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model IbuNifas."""
    queryset = IbuNifas.objects.all()
    serializer_class = IbuNifasSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ibu_hamil_id', 'posyandu_id', 'jenis_persalinan', 'tempat_persalinan', 'status']
    search_fields = ['ibu_hamil_id', 'posyandu_id', 'keluhan']
    ordering_fields = ['tanggal_persalinan', 'created_at']
    ordering = ['-tanggal_persalinan']
    
    @action(detail=False, methods=['get'])
    def by_ibu_hamil(self, request):
        """Mengambil data nifas berdasarkan ibu hamil."""
        ibu_hamil_id = request.query_params.get('ibu_hamil_id')
        if not ibu_hamil_id:
            return Response(
                {'error': 'ibu_hamil_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(ibu_hamil_id=ibu_hamil_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik ibu nifas."""
        total_nifas = self.queryset.count()
        by_kondisi = {
            'baik': self.queryset.filter(kondisi_ibu='baik').count(),
            'kurang_baik': self.queryset.filter(kondisi_ibu='kurang_baik').count(),
            'buruk': self.queryset.filter(kondisi_ibu='buruk').count(),
        }
        by_persalinan = {}
        for choice in IbuNifas.JENIS_PERSALINAN_CHOICES:
            by_persalinan[choice[0]] = self.queryset.filter(jenis_persalinan=choice[0]).count()
        
        return Response({
            'total_nifas': total_nifas,
            'by_kondisi': by_kondisi,
            'by_persalinan': by_persalinan,
        })


class BayiBaruLahirViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model BayiBaruLahir."""
    queryset = BayiBaruLahir.objects.all()
    serializer_class = BayiBaruLahirSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ibu_hamil_id', 'posyandu_id', 'jenis_kelamin', 'kondisi_lahir', 'status']
    search_fields = ['ibu_hamil_id', 'posyandu_id', 'catatan']
    ordering_fields = ['tanggal_lahir', 'created_at']
    ordering = ['-tanggal_lahir']
    
    @action(detail=False, methods=['get'])
    def by_ibu_hamil(self, request):
        """Mengambil data bayi berdasarkan ibu hamil."""
        ibu_hamil_id = request.query_params.get('ibu_hamil_id')
        if not ibu_hamil_id:
            return Response(
                {'error': 'ibu_hamil_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(ibu_hamil_id=ibu_hamil_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik bayi baru lahir."""
        total_bayi = self.queryset.count()
        by_kondisi = {
            'baik': self.queryset.filter(kondisi_lahir='baik').count(),
            'kurang_baik': self.queryset.filter(kondisi_lahir='kurang_baik').count(),
            'buruk': self.queryset.filter(kondisi_lahir='buruk').count(),
        }
        by_jenis_kelamin = {
            'laki_laki': self.queryset.filter(jenis_kelamin='Laki-laki').count(),
            'perempuan': self.queryset.filter(jenis_kelamin='Perempuan').count(),
        }
        by_status = {
            'hidup': self.queryset.filter(status='hidup').count(),
            'meninggal': self.queryset.filter(status='meninggal').count(),
        }
        
        return Response({
            'total_bayi': total_bayi,
            'by_kondisi': by_kondisi,
            'by_jenis_kelamin': by_jenis_kelamin,
            'by_status': by_status,
        })
