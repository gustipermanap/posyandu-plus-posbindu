"""
Views untuk risk-assessment-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from .models import RiskAssessment
from .serializers import RiskAssessmentSerializer, RiskAssessmentSearchSerializer


class RiskAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model RiskAssessment."""
    queryset = RiskAssessment.objects.all()
    serializer_class = RiskAssessmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit', 'jenis_penilaian', 'kategori_risiko']
    search_fields = ['visit__participant__nama_lengkap', 'jenis_penilaian', 'rekomendasi']
    ordering_fields = ['created_at', 'skor_total']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil penilaian risiko berdasarkan kunjungan."""
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
        """Mengambil penilaian risiko berdasarkan jenis penilaian."""
        jenis_penilaian = request.query_params.get('jenis_penilaian')
        if not jenis_penilaian:
            return Response(
                {'error': 'jenis_penilaian parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_penilaian=jenis_penilaian)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_kategori(self, request):
        """Mengambil penilaian risiko berdasarkan kategori risiko."""
        kategori_risiko = request.query_params.get('kategori_risiko')
        if not kategori_risiko:
            return Response(
                {'error': 'kategori_risiko parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(kategori_risiko=kategori_risiko)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """Mengambil penilaian risiko tinggi."""
        queryset = self.queryset.filter(kategori_risiko='Tinggi')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik penilaian risiko."""
        total_assessment = self.queryset.count()
        
        # Statistik berdasarkan kategori risiko
        by_kategori = {}
        for choice in RiskAssessment.KATEGORI_RISIKO_CHOICES:
            by_kategori[choice[0]] = self.queryset.filter(kategori_risiko=choice[0]).count()
        
        # Statistik berdasarkan jenis penilaian
        by_jenis = {}
        for choice in RiskAssessment.JENIS_PENILAIAN_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_penilaian=choice[0]).count()
        
        # Rata-rata skor
        avg_skor = self.queryset.aggregate(avg=Avg('skor_total'))['avg'] or 0
        
        return Response({
            'total_assessment': total_assessment,
            'by_kategori': by_kategori,
            'by_jenis': by_jenis,
            'rata_rata_skor': round(avg_skor, 2),
        })
