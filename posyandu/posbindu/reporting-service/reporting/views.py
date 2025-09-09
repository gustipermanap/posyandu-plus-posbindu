"""
Views untuk reporting-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import ReportLog, ActivityLog, DashboardData
from .serializers import ReportLogSerializer, ActivityLogSerializer, DashboardDataSerializer, ReportLogSearchSerializer


class ReportLogViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model ReportLog."""
    queryset = ReportLog.objects.all()
    serializer_class = ReportLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_laporan', 'status', 'tanggal_mulai', 'tanggal_akhir']
    search_fields = ['nama_laporan']
    ordering_fields = ['tanggal_mulai', 'tanggal_akhir', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil laporan berdasarkan jenis laporan."""
        jenis_laporan = request.query_params.get('jenis_laporan')
        if not jenis_laporan:
            return Response(
                {'error': 'jenis_laporan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_laporan=jenis_laporan)
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
        
        # Statistik berdasarkan jenis laporan
        by_jenis = {}
        for choice in ReportLog.JENIS_LAPORAN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_laporan=choice[0]).count()
        
        # Statistik berdasarkan status
        by_status = {}
        for choice in ReportLog.STATUS_CHOICES:
            by_status[choice[0]] = self.queryset.filter(status=choice[0]).count()
        
        return Response({
            'total_laporan': total_laporan,
            'by_jenis': by_jenis,
            'by_status': by_status,
        })


class ActivityLogViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model ActivityLog."""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id', 'modul', 'jenis_aktivitas']
    search_fields = ['deskripsi']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Mengambil log aktivitas berdasarkan user."""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(user_id=user_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_modul(self, request):
        """Mengambil log aktivitas berdasarkan modul."""
        modul = request.query_params.get('modul')
        if not modul:
            return Response(
                {'error': 'modul parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(modul=modul)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik log aktivitas."""
        total_activity = self.queryset.count()
        
        # Statistik berdasarkan modul
        by_modul = {}
        for choice in ActivityLog.MODUL_CHOICES:
            by_modul[choice[0]] = self.queryset.filter(modul=choice[0]).count()
        
        # Statistik berdasarkan jenis aktivitas
        by_jenis = {}
        for choice in ActivityLog.JENIS_AKTIVITAS_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_aktivitas=choice[0]).count()
        
        return Response({
            'total_activity': total_activity,
            'by_modul': by_modul,
            'by_jenis': by_jenis,
        })


class DashboardDataViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model DashboardData."""
    queryset = DashboardData.objects.all()
    serializer_class = DashboardDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Mengambil data dashboard terbaru."""
        queryset = self.queryset.order_by('-created_at')[:1]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
