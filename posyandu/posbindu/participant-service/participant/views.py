"""
Views untuk participant-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Participant, Visit, Location
from .serializers import (
    ParticipantSerializer, ParticipantListSerializer, VisitSerializer,
    LocationSerializer, ParticipantSearchSerializer
)


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Location."""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis', 'parent']
    search_fields = ['nama']
    ordering_fields = ['nama']
    ordering = ['nama']


class ParticipantViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Participant."""
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_kelamin', 'desa', 'status_merokok', 'status_alkohol', 'bpjs']
    search_fields = ['nik', 'nama_lengkap', 'no_hp']
    ordering_fields = ['nama_lengkap', 'created_at', 'tanggal_lahir']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Menggunakan serializer yang berbeda untuk list dan detail."""
        if self.action == 'list':
            return ParticipantListSerializer
        return ParticipantSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Pencarian peserta berdasarkan NIK, nama, atau nomor HP."""
        serializer = ParticipantSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.queryset
        nik = serializer.validated_data.get('nik')
        nama = serializer.validated_data.get('nama')
        no_hp = serializer.validated_data.get('no_hp')
        desa_id = serializer.validated_data.get('desa_id')
        
        if nik:
            queryset = queryset.filter(nik__icontains=nik)
        if nama:
            queryset = queryset.filter(nama_lengkap__icontains=nama)
        if no_hp:
            queryset = queryset.filter(no_hp__icontains=no_hp)
        if desa_id:
            queryset = queryset.filter(desa_id=desa_id)
        
        # Limit hasil untuk performa
        queryset = queryset[:50]
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_desa(self, request):
        """Mengambil peserta berdasarkan desa."""
        desa_id = request.query_params.get('desa_id')
        if not desa_id:
            return Response(
                {'error': 'desa_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(desa_id=desa_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik peserta."""
        total_participants = self.queryset.count()
        by_gender = {
            'laki_laki': self.queryset.filter(jenis_kelamin='Laki-laki').count(),
            'perempuan': self.queryset.filter(jenis_kelamin='Perempuan').count(),
        }
        by_smoking = {
            'tidak': self.queryset.filter(status_merokok='Tidak').count(),
            'aktif': self.queryset.filter(status_merokok='Aktif').count(),
            'eks': self.queryset.filter(status_merokok='Eks').count(),
        }
        by_bpjs = {
            'with_bpjs': self.queryset.filter(bpjs=True).count(),
            'without_bpjs': self.queryset.filter(bpjs=False).count(),
        }
        
        return Response({
            'total_participants': total_participants,
            'by_gender': by_gender,
            'by_smoking': by_smoking,
            'by_bpjs': by_bpjs,
        })


class VisitViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Visit."""
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['participant', 'pos_date', 'status', 'petugas_id']
    search_fields = ['participant__nama_lengkap', 'participant__nik']
    ordering_fields = ['pos_date', 'created_at']
    ordering = ['-pos_date', '-created_at']
    
    @action(detail=False, methods=['get'])
    def by_participant(self, request):
        """Mengambil kunjungan berdasarkan peserta."""
        participant_id = request.query_params.get('participant_id')
        if not participant_id:
            return Response(
                {'error': 'participant_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(participant_id=participant_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """Mengambil kunjungan berdasarkan rentang tanggal."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.queryset
        if start_date:
            queryset = queryset.filter(pos_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(pos_date__lte=end_date)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
