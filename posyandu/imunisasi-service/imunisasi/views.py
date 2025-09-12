"""
Views untuk imunisasi-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import JadwalImunisasi, PencatatanImunisasi, ReminderImunisasi, VaksinStock
from .serializers import (
    JadwalImunisasiSerializer, PencatatanImunisasiSerializer,
    ReminderImunisasiSerializer, VaksinStockSerializer, ImunisasiSearchSerializer
)


class JadwalImunisasiViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model JadwalImunisasi."""
    queryset = JadwalImunisasi.objects.all()
    serializer_class = JadwalImunisasiSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_imunisasi', 'aktif']
    search_fields = ['jenis_imunisasi', 'deskripsi']
    ordering_fields = ['usia_minimal_bulan', 'jenis_imunisasi']
    ordering = ['usia_minimal_bulan', 'jenis_imunisasi']
    
    @action(detail=False, methods=['get'])
    def by_usia(self, request):
        """Mengambil jadwal imunisasi berdasarkan usia."""
        usia_bulan = request.query_params.get('usia_bulan')
        if not usia_bulan:
            return Response(
                {'error': 'usia_bulan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usia = int(usia_bulan)
        except ValueError:
            return Response(
                {'error': 'usia_bulan must be a valid integer'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(
            usia_minimal_bulan__lte=usia,
            usia_maksimal_bulan__gte=usia,
            aktif=True
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PencatatanImunisasiViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model PencatatanImunisasi."""
    queryset = PencatatanImunisasi.objects.all()
    serializer_class = PencatatanImunisasiSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balita_id', 'posyandu_id', 'jenis_imunisasi', 'status', 'tanggal_pemberian']
    search_fields = ['balita_id', 'posyandu_id', 'petugas_pemberian', 'batch_vaksin']
    ordering_fields = ['tanggal_pemberian', 'created_at']
    ordering = ['-tanggal_pemberian']
    
    @action(detail=False, methods=['get'])
    def by_balita(self, request):
        """Mengambil pencatatan imunisasi berdasarkan balita."""
        balita_id = request.query_params.get('balita_id')
        if not balita_id:
            return Response(
                {'error': 'balita_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(balita_id=balita_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil pencatatan imunisasi berdasarkan jenis."""
        jenis_imunisasi = request.query_params.get('jenis_imunisasi')
        if not jenis_imunisasi:
            return Response(
                {'error': 'jenis_imunisasi parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_imunisasi=jenis_imunisasi)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik pencatatan imunisasi."""
        total_pencatatan = self.queryset.count()
        by_status = {
            'diberikan': self.queryset.filter(status='diberikan').count(),
            'tidak_diberikan': self.queryset.filter(status='tidak_diberikan').count(),
            'kontraindikasi': self.queryset.filter(status='kontraindikasi').count(),
            'menolak': self.queryset.filter(status='menolak').count(),
        }
        by_jenis = {}
        for choice in PencatatanImunisasi.JENIS_IMUNISASI_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_imunisasi=choice[0]).count()
        
        return Response({
            'total_pencatatan': total_pencatatan,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })


class ReminderImunisasiViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model ReminderImunisasi."""
    queryset = ReminderImunisasi.objects.all()
    serializer_class = ReminderImunisasiSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['balita_id', 'posyandu_id', 'jenis_imunisasi', 'status', 'prioritas']
    search_fields = ['balita_id', 'posyandu_id', 'catatan']
    ordering_fields = ['prioritas', 'tanggal_reminder', 'created_at']
    ordering = ['prioritas', '-tanggal_reminder']
    
    @action(detail=False, methods=['get'])
    def by_balita(self, request):
        """Mengambil reminder berdasarkan balita."""
        balita_id = request.query_params.get('balita_id')
        if not balita_id:
            return Response(
                {'error': 'balita_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(balita_id=balita_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_prioritas(self, request):
        """Mengambil reminder berdasarkan prioritas."""
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
    def statistics(self, request):
        """Statistik reminder imunisasi."""
        total_reminder = self.queryset.count()
        by_status = {
            'belum_jadwal': self.queryset.filter(status='belum_jadwal').count(),
            'sudah_jadwal': self.queryset.filter(status='sudah_jadwal').count(),
            'terlambat': self.queryset.filter(status='terlambat').count(),
            'diberikan': self.queryset.filter(status='diberikan').count(),
        }
        by_prioritas = {
            'rendah': self.queryset.filter(prioritas='rendah').count(),
            'sedang': self.queryset.filter(prioritas='sedang').count(),
            'tinggi': self.queryset.filter(prioritas='tinggi').count(),
            'urgent': self.queryset.filter(prioritas='urgent').count(),
        }
        
        return Response({
            'total_reminder': total_reminder,
            'by_status': by_status,
            'by_prioritas': by_prioritas,
        })


class VaksinStockViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model VaksinStock."""
    queryset = VaksinStock.objects.all()
    serializer_class = VaksinStockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_vaksin', 'status', 'supplier']
    search_fields = ['jenis_vaksin', 'batch_number', 'supplier']
    ordering_fields = ['jenis_vaksin', 'tanggal_kedaluwarsa', 'created_at']
    ordering = ['jenis_vaksin', 'tanggal_kedaluwarsa']
    
    @action(detail=False, methods=['get'])
    def by_jenis(self, request):
        """Mengambil stok berdasarkan jenis vaksin."""
        jenis_vaksin = request.query_params.get('jenis_vaksin')
        if not jenis_vaksin:
            return Response(
                {'error': 'jenis_vaksin parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_vaksin=jenis_vaksin)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Mengambil vaksin yang akan kedaluwarsa dalam 30 hari."""
        queryset = self.queryset.filter(status='tersedia')
        expiring_vaccines = []
        for vaccine in queryset:
            if vaccine.is_expiring_soon:
                expiring_vaccines.append(vaccine)
        
        page = self.paginate_queryset(expiring_vaccines)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(expiring_vaccines, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik stok vaksin."""
        total_stok = self.queryset.count()
        by_status = {
            'tersedia': self.queryset.filter(status='tersedia').count(),
            'habis': self.queryset.filter(status='habis').count(),
            'kedaluwarsa': self.queryset.filter(status='kedaluwarsa').count(),
        }
        by_jenis = {}
        for vaccine in self.queryset.values('jenis_vaksin').distinct():
            jenis = vaccine['jenis_vaksin']
            by_jenis[jenis] = self.queryset.filter(jenis_vaksin=jenis).count()
        
        return Response({
            'total_stok': total_stok,
            'by_status': by_status,
            'by_jenis': by_jenis,
        })
