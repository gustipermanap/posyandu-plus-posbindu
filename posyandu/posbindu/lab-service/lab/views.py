"""
Views untuk lab-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import LabExamination, StockStrip
from .serializers import LabExaminationSerializer, StockStripSerializer, LabExaminationSearchSerializer


class LabExaminationViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model LabExamination."""
    queryset = LabExamination.objects.all()
    serializer_class = LabExaminationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit_id', 'jenis_pemeriksaan']
    search_fields = ['participant_id', 'jenis_pemeriksaan']
    ordering_fields = ['waktu_ambil', 'created_at']
    ordering = ['-waktu_ambil']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil hasil lab berdasarkan kunjungan."""
        visit_id = request.query_params.get('visit_id')
        if not visit_id:
            return Response(
                {'error': 'visit_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(visit_id=visit_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil hasil lab berdasarkan jenis pemeriksaan."""
        jenis_pemeriksaan = request.query_params.get('jenis_pemeriksaan')
        if not jenis_pemeriksaan:
            return Response(
                {'error': 'jenis_pemeriksaan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_pemeriksaan=jenis_pemeriksaan)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Mengambil hasil lab berdasarkan status."""
        status_lab = request.query_params.get('status')
        if not status_lab:
            return Response(
                {'error': 'status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(status=status_lab)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik hasil lab."""
        total_lab_result = self.queryset.count()
        
        # Statistik berdasarkan status
        by_status = {}
        for choice in LabResult.STATUS_CHOICES:
            by_status[choice[0]] = self.queryset.filter(status=choice[0]).count()
        
        # Top jenis pemeriksaan
        top_jenis = self.queryset.values('jenis_pemeriksaan').annotate(
            count=Count('jenis_pemeriksaan')
        ).order_by('-count')[:10]
        
        return Response({
            'total_lab_result': total_lab_result,
            'by_status': by_status,
            'top_jenis': list(top_jenis),
        })


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Stock."""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_item', 'supplier']
    search_fields = ['nama_item', 'supplier']
    ordering_fields = ['nama_item', 'tanggal_kadaluarsa']
    ordering = ['nama_item']
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil stok berdasarkan jenis item."""
        jenis_item = request.query_params.get('jenis_item')
        if not jenis_item:
            return Response(
                {'error': 'jenis_item parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_item=jenis_item)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Mengambil item dengan stok rendah."""
        threshold = request.query_params.get('threshold', 10)
        queryset = self.queryset.filter(stok_tersisa__lte=threshold)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Mengambil item yang akan kadaluarsa."""
        from datetime import date, timedelta
        days_ahead = request.query_params.get('days_ahead', 30)
        future_date = date.today() + timedelta(days=int(days_ahead))
        
        queryset = self.queryset.filter(tanggal_kadaluarsa__lte=future_date)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik stok."""
        total_stock = self.queryset.count()
        
        # Statistik berdasarkan jenis item
        by_jenis = {}
        for choice in Stock.JENIS_ITEM_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_item=choice[0]).count()
        
        # Stok rendah
        low_stock_count = self.queryset.filter(stok_tersisa__lte=10).count()
        
        return Response({
            'total_stock': total_stock,
            'by_jenis': by_jenis,
            'low_stock_count': low_stock_count,
        })
