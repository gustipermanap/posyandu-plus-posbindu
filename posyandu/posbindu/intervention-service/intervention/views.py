"""
Views untuk intervention-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Intervention
from .serializers import InterventionSerializer, InterventionSearchSerializer


class InterventionViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Intervention."""
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit', 'jenis_intervensi', 'status']
    search_fields = ['visit__participant__nama_lengkap', 'jenis_intervensi', 'deskripsi']
    ordering_fields = ['created_at', 'durasi']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil intervensi berdasarkan kunjungan."""
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
        """Mengambil intervensi berdasarkan jenis intervensi."""
        jenis_intervensi = request.query_params.get('jenis_intervensi')
        if not jenis_intervensi:
            return Response(
                {'error': 'jenis_intervensi parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_intervensi=jenis_intervensi)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Mengambil intervensi berdasarkan status."""
        status_intervensi = request.query_params.get('status')
        if not status_intervensi:
            return Response(
                {'error': 'status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(status=status_intervensi)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Mengambil intervensi yang sedang aktif."""
        queryset = self.queryset.filter(status='Aktif')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Mengambil intervensi yang sudah selesai."""
        queryset = self.queryset.filter(status='Selesai')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik intervensi."""
        total_intervention = self.queryset.count()
        
        # Statistik berdasarkan status
        by_status = {}
        for choice in Intervention.STATUS_CHOICES:
            by_status[choice[0]] = self.queryset.filter(status=choice[0]).count()
        
        # Statistik berdasarkan jenis intervensi
        by_jenis = {}
        for choice in Intervention.JENIS_INTERVENSI_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_intervensi=choice[0]).count()
        
        return Response({
            'total_intervention': total_intervention,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })
