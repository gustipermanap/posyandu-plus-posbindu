"""
Views untuk vitamin-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import JenisVitamin, PemberianVitamin, PMT, StokVitamin, StokPMT
from .serializers import (
    JenisVitaminSerializer, PemberianVitaminSerializer, PMTSerializer,
    StokVitaminSerializer, StokPMTSerializer, VitaminSearchSerializer
)


class JenisVitaminViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model JenisVitamin."""
    queryset = JenisVitamin.objects.all()
    serializer_class = JenisVitaminSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_vitamin', 'aktif']
    search_fields = ['jenis_vitamin', 'deskripsi']
    ordering_fields = ['jenis_vitamin']
    ordering = ['jenis_vitamin']
    
    @action(detail=False, methods=['get'])
    def aktif(self, request):
        """Mengambil jenis vitamin yang aktif."""
        queryset = self.queryset.filter(aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PemberianVitaminViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PemberianVitamin."""
    queryset = PemberianVitamin.objects.all()
    serializer_class = PemberianVitaminSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['penerima_id', 'posyandu_id', 'jenis_penerima', 'jenis_vitamin', 'status', 'tanggal_pemberian']
    search_fields = ['penerima_id', 'posyandu_id', 'petugas_pemberian']
    ordering_fields = ['tanggal_pemberian', 'created_at']
    ordering = ['-tanggal_pemberian']
    
    @action(detail=False, methods=['get'])
    def by_penerima(self, request):
        """Mengambil pemberian vitamin berdasarkan penerima."""
        penerima_id = request.query_params.get('penerima_id')
        if not penerima_id:
            return Response(
                {'error': 'penerima_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(penerima_id=penerima_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil pemberian vitamin berdasarkan jenis."""
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
        """Statistik pemberian vitamin."""
        total_pemberian = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in PemberianVitamin.JENIS_VITAMIN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_vitamin=choice[0]).count()
        
        return Response({
            'total_pemberian': total_pemberian,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class PMTViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PMT."""
    queryset = PMT.objects.all()
    serializer_class = PMTSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['penerima_id', 'posyandu_id', 'jenis_penerima', 'jenis_pmt', 'status', 'tanggal_pemberian']
    search_fields = ['penerima_id', 'posyandu_id', 'petugas_pemberian']
    ordering_fields = ['tanggal_pemberian', 'created_at']
    ordering = ['-tanggal_pemberian']
    
    @action(detail=False, methods=['get'])
    def by_penerima(self, request):
        """Mengambil PMT berdasarkan penerima."""
        penerima_id = request.query_params.get('penerima_id')
        if not penerima_id:
            return Response(
                {'error': 'penerima_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(penerima_id=penerima_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil PMT berdasarkan jenis."""
        jenis_pmt = request.query_params.get('jenis_pmt')
        if not jenis_pmt:
            return Response(
                {'error': 'jenis_pmt parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_pmt=jenis_pmt)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik PMT."""
        total_pmt = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in PMT.JENIS_PMT_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_pmt=choice[0]).count()
        
        return Response({
            'total_pmt': total_pmt,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class StokVitaminViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model StokVitamin."""
    queryset = StokVitamin.objects.all()
    serializer_class = StokVitaminSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_vitamin', 'status', 'supplier']
    search_fields = ['jenis_vitamin', 'nama_produk', 'batch_number', 'supplier']
    ordering_fields = ['jenis_vitamin', 'tanggal_kedaluwarsa', 'created_at']
    ordering = ['jenis_vitamin', 'tanggal_kedaluwarsa']
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil stok berdasarkan jenis vitamin."""
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
    def expiring_soon(self, request):
        """Mengambil stok yang akan kedaluwarsa dalam 30 hari."""
        queryset = self.queryset.filter(status='tersedia')
        expiring_items = []
        for item in queryset:
            if item.is_expiring_soon:
                expiring_items.append(item)
        
        page = self.paginate_queryset(expiring_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(expiring_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik stok vitamin."""
        total_stok = self.queryset.count()
        by_status = {
            'tersedia': self.queryset.filter(status='tersedia').count(),
            'habis': self.queryset.filter(status='habis').count(),
            'kedaluwarsa': self.queryset.filter(status='kedaluwarsa').count(),
        }
        by_jenis = {}
        for choice in StokVitamin.JENIS_VITAMIN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_vitamin=choice[0]).count()
        
        return Response({
            'total_stok': total_stok,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class StokPMTViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model StokPMT."""
    queryset = StokPMT.objects.all()
    serializer_class = StokPMTSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_pmt', 'status', 'supplier']
    search_fields = ['jenis_pmt', 'nama_produk', 'batch_number', 'supplier']
    ordering_fields = ['jenis_pmt', 'tanggal_kedaluwarsa', 'created_at']
    ordering = ['jenis_pmt', 'tanggal_kedaluwarsa']
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil stok berdasarkan jenis PMT."""
        jenis_pmt = request.query_params.get('jenis_pmt')
        if not jenis_pmt:
            return Response(
                {'error': 'jenis_pmt parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_pmt=jenis_pmt)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Mengambil stok yang akan kedaluwarsa dalam 30 hari."""
        queryset = self.queryset.filter(status='tersedia')
        expiring_items = []
        for item in queryset:
            if item.is_expiring_soon:
                expiring_items.append(item)
        
        page = self.paginate_queryset(expiring_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(expiring_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik stok PMT."""
        total_stok = self.queryset.count()
        by_status = {
            'tersedia': self.queryset.filter(status='tersedia').count(),
            'habis': self.queryset.filter(status='habis').count(),
            'kedaluwarsa': self.queryset.filter(status='kedaluwarsa').count(),
        }
        by_jenis = {}
        for choice in StokPMT.JENIS_PMT_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_pmt=choice[0]).count()
        
        return Response({
            'total_stok': total_stok,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })
