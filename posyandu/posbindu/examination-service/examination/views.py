"""
Views untuk examination-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Max, Min
from .models import VitalSigns, Anthropometry
from .serializers import VitalSignsSerializer, AnthropometrySerializer, VitalSignsSearchSerializer


class VitalSignsViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model VitalSigns."""
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit_id', 'td_sistol_rerata', 'td_diastol_rerata']
    search_fields = ['participant_id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil vital sign berdasarkan kunjungan."""
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
    def by_pressure_range(self, request):
        """Mengambil vital sign berdasarkan range tekanan darah."""
        sistol_min = request.query_params.get('sistol_min')
        sistol_max = request.query_params.get('sistol_max')
        diastol_min = request.query_params.get('diastol_min')
        diastol_max = request.query_params.get('diastol_max')
        
        queryset = self.queryset.all()
        
        if sistol_min:
            queryset = queryset.filter(sistol__gte=sistol_min)
        if sistol_max:
            queryset = queryset.filter(sistol__lte=sistol_max)
        if diastol_min:
            queryset = queryset.filter(diastol__gte=diastol_min)
        if diastol_max:
            queryset = queryset.filter(diastol__lte=diastol_max)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik vital sign."""
        total_vital_sign = self.queryset.count()
        
        # Rata-rata vital sign
        avg_sistol = self.queryset.aggregate(avg=Avg('sistol'))['avg'] or 0
        avg_diastol = self.queryset.aggregate(avg=Avg('diastol'))['avg'] or 0
        avg_nadi = self.queryset.aggregate(avg=Avg('nadi'))['avg'] or 0
        avg_suhu = self.queryset.aggregate(avg=Avg('suhu'))['avg'] or 0
        
        # Range vital sign
        sistol_range = self.queryset.aggregate(
            min=Min('sistol'), max=Max('sistol')
        )
        diastol_range = self.queryset.aggregate(
            min=Min('diastol'), max=Max('diastol')
        )
        
        return Response({
            'total_vital_sign': total_vital_sign,
            'rata_rata': {
                'sistol': round(avg_sistol, 2),
                'diastol': round(avg_diastol, 2),
                'nadi': round(avg_nadi, 2),
                'suhu': round(avg_suhu, 2),
            },
            'range': {
                'sistol': sistol_range,
                'diastol': diastol_range,
            }
        })


class AnthropometryViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Anthropometry."""
    queryset = Anthropometry.objects.all()
    serializer_class = AnthropometrySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['visit']
    search_fields = ['visit__participant__nama_lengkap']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_visit(self, request):
        """Mengambil antropometri berdasarkan kunjungan."""
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
    def statistics(self, request):
        """Statistik antropometri."""
        total_anthropometry = self.queryset.count()
        
        # Rata-rata antropometri
        avg_berat = self.queryset.aggregate(avg=Avg('berat_badan'))['avg'] or 0
        avg_tinggi = self.queryset.aggregate(avg=Avg('tinggi_badan'))['avg'] or 0
        avg_lingkar_pinggang = self.queryset.aggregate(avg=Avg('lingkar_pinggang'))['avg'] or 0
        avg_lingkar_pinggul = self.queryset.aggregate(avg=Avg('lingkar_pinggul'))['avg'] or 0
        
        return Response({
            'total_anthropometry': total_anthropometry,
            'rata_rata': {
                'berat_badan': round(avg_berat, 2),
                'tinggi_badan': round(avg_tinggi, 2),
                'lingkar_pinggang': round(avg_lingkar_pinggang, 2),
                'lingkar_pinggul': round(avg_lingkar_pinggul, 2),
            }
        })
