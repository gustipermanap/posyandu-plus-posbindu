"""
Views untuk screening-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Anamnesis
from .serializers import AnamnesisSerializer, AnamnesisSearchSerializer


class AnamnesisViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Anamnesis."""
    queryset = Anamnesis.objects.all()
    serializer_class = AnamnesisSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit', 'keluhan_utama']
    search_fields = ['visit__participant__nama_lengkap', 'keluhan_utama', 'keluhan_tambahan']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_participant(self, request):
        """Mengambil anamnesis berdasarkan peserta."""
        participant_id = request.query_params.get('participant_id')
        if not participant_id:
            return Response(
                {'error': 'participant_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(visit__participant_id=participant_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_keluhan(self, request):
        """Mengambil anamnesis berdasarkan keluhan."""
        keluhan = request.query_params.get('keluhan')
        if not keluhan:
            return Response(
                {'error': 'keluhan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(
            Q(keluhan_utama__icontains=keluhan) | 
            Q(keluhan_tambahan__icontains=keluhan)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik anamnesis."""
        total_anamnesis = self.queryset.count()
        
        # Top keluhan utama
        from django.db.models import Count
        top_keluhan = self.queryset.values('keluhan_utama').annotate(
            count=Count('keluhan_utama')
        ).order_by('-count')[:10]
        
        return Response({
            'total_anamnesis': total_anamnesis,
            'top_keluhan': list(top_keluhan),
        })
