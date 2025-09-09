"""
Views untuk laporan-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import TemplateLaporan, Laporan, StatistikPosyandu, DashboardData, ExportLog
from .serializers import (
    TemplateLaporanSerializer, LaporanSerializer, StatistikPosyanduSerializer,
    DashboardDataSerializer, ExportLogSerializer, LaporanSearchSerializer
)


class TemplateLaporanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model TemplateLaporan."""
    queryset = TemplateLaporan.objects.all()
    serializer_class = TemplateLaporanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_laporan', 'kategori_laporan', 'aktif']
    search_fields = ['nama_template', 'jenis_laporan', 'kategori_laporan']
    ordering_fields = ['nama_template', 'jenis_laporan', 'kategori_laporan']
    ordering = ['nama_template']
    
    @action(detail=False, methods=['get'])
    def aktif(self, request):
        """Mengambil template laporan yang aktif."""
        queryset = self.queryset.filter(aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_kategori(self, request):
        """Mengambil template berdasarkan kategori."""
        kategori_laporan = request.query_params.get('kategori_laporan')
        if not kategori_laporan:
            return Response(
                {'error': 'kategori_laporan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(kategori_laporan=kategori_laporan, aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik template laporan."""
        total_template = self.queryset.count()
        by_jenis = {}
        for choice in TemplateLaporan.JENIS_LAPORAN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_laporan=choice[0]).count()
        
        by_kategori = {}
        for choice in TemplateLaporan.KATEGORI_LAPORAN_CHOICES:
            by_kategori[choice[0]] = self.queryset.filter(kategori_laporan=choice[0]).count()
        
        by_status = {
            'aktif': self.queryset.filter(aktif=True).count(),
            'tidak_aktif': self.queryset.filter(aktif=False).count(),
        }
        
        return Response({
            'total_template': total_template,
            'by_jenis': by_jenis,
            'by_kategori': by_kategori,
            'by_status': by_status,
        })


class LaporanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Laporan."""
    queryset = Laporan.objects.all()
    serializer_class = LaporanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['posyandu_id', 'template', 'status', 'tanggal_mulai', 'tanggal_akhir']
    search_fields = ['posyandu_id', 'nama_laporan']
    ordering_fields = ['tanggal_mulai', 'tanggal_akhir', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_posyandu(self, request):
        """Mengambil laporan berdasarkan posyandu."""
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
    def by_status(self, request):
        """Mengambil laporan berdasarkan status."""
        status_laporan = request.query_params.get('status')
        if not status_laporan:
            return Response(
                {'error': 'status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(status=status_laporan)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik laporan."""
        total_laporan = self.queryset.count()
        by_status = {
            'draft': self.queryset.filter(status='draft').count(),
            'final': self.queryset.filter(status='final').count(),
            'published': self.queryset.filter(status='published').count(),
            'archived': self.queryset.filter(status='archived').count(),
        }
        
        return Response({
            'total_laporan': total_laporan,
            'by_status': by_status,
        })


class StatistikPosyanduViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model StatistikPosyandu."""
    queryset = StatistikPosyandu.objects.all()
    serializer_class = StatistikPosyanduSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['posyandu_id', 'tanggal_statistik']
    search_fields = ['posyandu_id']
    ordering_fields = ['tanggal_statistik', 'created_at']
    ordering = ['-tanggal_statistik']
    
    @action(detail=False, methods=['get'])
    def by_posyandu(self, request):
        """Mengambil statistik berdasarkan posyandu."""
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
    def latest(self, request):
        """Mengambil statistik terbaru."""
        posyandu_id = request.query_params.get('posyandu_id')
        if posyandu_id:
            queryset = self.queryset.filter(posyandu_id=posyandu_id).order_by('-tanggal_statistik')[:1]
        else:
            queryset = self.queryset.order_by('-tanggal_statistik')[:10]
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik statistik posyandu."""
        total_statistik = self.queryset.count()
        
        # Rata-rata statistik
        avg_balita = self.queryset.aggregate(avg=models.Avg('total_balita'))['avg'] or 0
        avg_ibu_hamil = self.queryset.aggregate(avg=models.Avg('total_ibu_hamil'))['avg'] or 0
        avg_imunisasi = self.queryset.aggregate(avg=models.Avg('total_imunisasi'))['avg'] or 0
        avg_kb = self.queryset.aggregate(avg=models.Avg('total_wus'))['avg'] or 0
        
        return Response({
            'total_statistik': total_statistik,
            'rata_rata': {
                'balita': round(avg_balita, 2),
                'ibu_hamil': round(avg_ibu_hamil, 2),
                'imunisasi': round(avg_imunisasi, 2),
                'kb': round(avg_kb, 2),
            }
        })


class DashboardDataViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model DashboardData."""
    queryset = DashboardData.objects.all()
    serializer_class = DashboardDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['posyandu_id', 'tanggal_data']
    search_fields = ['posyandu_id']
    ordering_fields = ['tanggal_data', 'created_at']
    ordering = ['-tanggal_data']
    
    @action(detail=False, methods=['get'])
    def by_posyandu(self, request):
        """Mengambil dashboard data berdasarkan posyandu."""
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
    def latest(self, request):
        """Mengambil dashboard data terbaru."""
        posyandu_id = request.query_params.get('posyandu_id')
        if posyandu_id:
            queryset = self.queryset.filter(posyandu_id=posyandu_id).order_by('-tanggal_data')[:1]
        else:
            queryset = self.queryset.order_by('-tanggal_data')[:10]
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExportLogViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model ExportLog."""
    queryset = ExportLog.objects.all()
    serializer_class = ExportLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['laporan', 'format_export', 'status']
    search_fields = ['laporan__nama_laporan']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_laporan(self, request):
        """Mengambil export log berdasarkan laporan."""
        laporan_id = request.query_params.get('laporan_id')
        if not laporan_id:
            return Response(
                {'error': 'laporan_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(laporan_id=laporan_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_format(self, request):
        """Mengambil export log berdasarkan format."""
        format_export = request.query_params.get('format_export')
        if not format_export:
            return Response(
                {'error': 'format_export parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(format_export=format_export)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik export log."""
        total_export = self.queryset.count()
        by_format = {}
        for choice in ExportLog.FORMAT_EXPORT_CHOICES:
            by_format[choice[0]] = self.queryset.filter(format_export=choice[0]).count()
        
        by_status = {
            'processing': self.queryset.filter(status='processing').count(),
            'completed': self.queryset.filter(status='completed').count(),
            'failed': self.queryset.filter(status='failed').count(),
        }
        
        return Response({
            'total_export': total_export,
            'by_format': by_format,
            'by_status': by_status,
        })
