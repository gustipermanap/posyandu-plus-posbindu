"""
Views untuk kb-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import MetodeKB, PencatatanKB, KonselingKB, StokKB, RujukanKB
from .serializers import (
    MetodeKBSerializer, PencatatanKBSerializer, KonselingKBSerializer,
    StokKBSerializer, RujukanKBSerializer, KBSearchSerializer
)


class MetodeKBViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model MetodeKB."""
    queryset = MetodeKB.objects.all()
    serializer_class = MetodeKBSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_metode', 'aktif']
    search_fields = ['jenis_metode', 'deskripsi']
    ordering_fields = ['jenis_metode', 'efektivitas_percent']
    ordering = ['jenis_metode']
    
    @action(detail=False, methods=['get'])
    def aktif(self, request):
        """Mengambil metode KB yang aktif."""
        queryset = self.queryset.filter(aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PencatatanKBViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PencatatanKB."""
    queryset = PencatatanKB.objects.all()
    serializer_class = PencatatanKBSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['wus_id', 'posyandu_id', 'metode_kb', 'status', 'tanggal_mulai']
    search_fields = ['wus_id', 'posyandu_id', 'petugas_kb']
    ordering_fields = ['tanggal_mulai', 'created_at']
    ordering = ['-tanggal_mulai']
    
    @action(detail=False, methods=['get'])
    def by_wus(self, request):
        """Mengambil pencatatan KB berdasarkan WUS."""
        wus_id = request.query_params.get('wus_id')
        if not wus_id:
            return Response(
                {'error': 'wus_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(wus_id=wus_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_metode(self, request):
        """Mengambil pencatatan KB berdasarkan metode."""
        metode_kb = request.query_params.get('metode_kb')
        if not metode_kb:
            return Response(
                {'error': 'metode_kb parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(metode_kb=metode_kb)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik pencatatan KB."""
        total_pencatatan = self.queryset.count()
        by_status = {
            'aktif': self.queryset.filter(status='aktif').count(),
            'tidak_aktif': self.queryset.filter(status='tidak_aktif').count(),
            'ganti_metode': self.queryset.filter(status='ganti_metode').count(),
            'hamil': self.queryset.filter(status='hamil').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_metode = {}
        for choice in PencatatanKB.JENIS_METODE_CHOICES:
            by_metode[choice[0]] = self.queryset.filter(metode_kb=choice[0]).count()
        
        return Response({
            'total_pencatatan': total_pencatatan,
            'by_status': by_status,
            'by_metode': by_metode,
        })


class KonselingKBViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model KonselingKB."""
    queryset = KonselingKB.objects.all()
    serializer_class = KonselingKBSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['wus_id', 'posyandu_id', 'jenis_konseling', 'status', 'tanggal_konseling']
    search_fields = ['wus_id', 'posyandu_id', 'topik_konseling', 'petugas_konseling']
    ordering_fields = ['tanggal_konseling', 'created_at']
    ordering = ['-tanggal_konseling']
    
    @action(detail=False, methods=['get'])
    def by_wus(self, request):
        """Mengambil konseling berdasarkan WUS."""
        wus_id = request.query_params.get('wus_id')
        if not wus_id:
            return Response(
                {'error': 'wus_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(wus_id=wus_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil konseling berdasarkan jenis."""
        jenis_konseling = request.query_params.get('jenis_konseling')
        if not jenis_konseling:
            return Response(
                {'error': 'jenis_konseling parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_konseling=jenis_konseling)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik konseling KB."""
        total_konseling = self.queryset.count()
        by_jenis = {
            'awal': self.queryset.filter(jenis_konseling='awal').count(),
            'kontrol': self.queryset.filter(jenis_konseling='kontrol').count(),
            'ganti_metode': self.queryset.filter(jenis_konseling='ganti_metode').count(),
            'efek_samping': self.queryset.filter(jenis_konseling='efek_samping').count(),
            'hamil': self.queryset.filter(jenis_konseling='hamil').count(),
        }
        by_status = {
            'selesai': self.queryset.filter(status='selesai').count(),
            'tindak_lanjut': self.queryset.filter(status='tindak_lanjut').count(),
            'rujukan': self.queryset.filter(status='rujukan').count(),
        }
        
        return Response({
            'total_konseling': total_konseling,
            'by_jenis': by_jenis,
            'by_status': by_status,
        })


class StokKBViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model StokKB."""
    queryset = StokKB.objects.all()
    serializer_class = StokKBSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_alat', 'metode_kb', 'status', 'supplier']
    search_fields = ['jenis_alat', 'batch_number', 'supplier']
    ordering_fields = ['jenis_alat', 'tanggal_kedaluwarsa', 'created_at']
    ordering = ['jenis_alat', 'tanggal_kedaluwarsa']
    
    @action(detail=False, methods=['get'])
    def by_metode(self, request):
        """Mengambil stok berdasarkan metode KB."""
        metode_kb = request.query_params.get('metode_kb')
        if not metode_kb:
            return Response(
                {'error': 'metode_kb parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(metode_kb=metode_kb)
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
        """Statistik stok KB."""
        total_stok = self.queryset.count()
        by_status = {
            'tersedia': self.queryset.filter(status='tersedia').count(),
            'habis': self.queryset.filter(status='habis').count(),
            'kedaluwarsa': self.queryset.filter(status='kedaluwarsa').count(),
        }
        by_metode = {}
        for choice in StokKB.JENIS_METODE_CHOICES:
            by_metode[choice[0]] = self.queryset.filter(metode_kb=choice[0]).count()
        
        return Response({
            'total_stok': total_stok,
            'by_status': by_status,
            'by_metode': by_metode,
        })


class RujukanKBViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model RujukanKB."""
    queryset = RujukanKB.objects.all()
    serializer_class = RujukanKBSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['wus_id', 'posyandu_id', 'status', 'tanggal_rujukan']
    search_fields = ['wus_id', 'posyandu_id', 'tujuan_rujukan', 'petugas_rujukan']
    ordering_fields = ['tanggal_rujukan', 'created_at']
    ordering = ['-tanggal_rujukan']
    
    @action(detail=False, methods=['get'])
    def by_wus(self, request):
        """Mengambil rujukan berdasarkan WUS."""
        wus_id = request.query_params.get('wus_id')
        if not wus_id:
            return Response(
                {'error': 'wus_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(wus_id=wus_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Mengambil rujukan berdasarkan status."""
        status_rujukan = request.query_params.get('status')
        if not status_rujukan:
            return Response(
                {'error': 'status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(status=status_rujukan)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik rujukan KB."""
        total_rujukan = self.queryset.count()
        by_status = {
            'dikirim': self.queryset.filter(status='dikirim').count(),
            'diterima': self.queryset.filter(status='diterima').count(),
            'selesai': self.queryset.filter(status='selesai').count(),
            'ditolak': self.queryset.filter(status='ditolak').count(),
        }
        
        return Response({
            'total_rujukan': total_rujukan,
            'by_status': by_status,
        })
