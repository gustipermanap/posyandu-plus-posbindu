"""
Views untuk referral-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Referral
from .serializers import ReferralSerializer, ReferralSearchSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Referral."""
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit', 'fasilitas_tujuan', 'status', 'prioritas']
    search_fields = ['visit__participant__nama_lengkap', 'fasilitas_tujuan', 'alasan_rujukan']
    ordering_fields = ['tanggal_rujukan', 'created_at']
    ordering = ['-tanggal_rujukan']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil rujukan berdasarkan kunjungan."""
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
    def by_fasilitas(self, request):
        """Mengambil rujukan berdasarkan fasilitas tujuan."""
        fasilitas_tujuan = request.query_params.get('fasilitas_tujuan')
        if not fasilitas_tujuan:
            return Response(
                {'error': 'fasilitas_tujuan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(fasilitas_tujuan=fasilitas_tujuan)
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
    def by_prioritas(self, request):
        """Mengambil rujukan berdasarkan prioritas."""
        prioritas = request.query_params.get('prioritas')
        if not prioritas:
            return Response(
                {'error': 'prioritas parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(prioritas=prioritas)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Mengambil rujukan yang pending."""
        queryset = self.queryset.filter(status='Pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Mengambil rujukan yang sudah selesai."""
        queryset = self.queryset.filter(status='Selesai')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik rujukan."""
        total_referral = self.queryset.count()
        
        # Statistik berdasarkan status
        by_status = {}
        for choice in Referral.STATUS_CHOICES:
            by_status[choice[0]] = self.queryset.filter(status=choice[0]).count()
        
        # Statistik berdasarkan prioritas
        by_prioritas = {}
        for choice in Referral.PRIORITAS_CHOICES:
            by_prioritas[choice[0]] = self.queryset.filter(prioritas=choice[0]).count()
        
        # Top fasilitas tujuan
        top_fasilitas = self.queryset.values('fasilitas_tujuan').annotate(
            count=Count('fasilitas_tujuan')
        ).order_by('-count')[:10]
        
        return Response({
            'total_referral': total_referral,
            'by_status': by_status,
            'by_prioritas': by_prioritas,
            'top_fasilitas': list(top_fasilitas),
        })
