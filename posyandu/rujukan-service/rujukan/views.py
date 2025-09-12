"""
Views untuk rujukan-service.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import FasilitasKesehatan, Rujukan, FollowUpRujukan, TemplateRujukan
from .serializers import (
    FasilitasKesehatanSerializer, RujukanSerializer, FollowUpRujukanSerializer,
    TemplateRujukanSerializer, RujukanSearchSerializer
)


class FasilitasKesehatanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model FasilitasKesehatan."""
    queryset = FasilitasKesehatan.objects.all()
    serializer_class = FasilitasKesehatanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_fasilitas', 'level_fasilitas', 'aktif']
    search_fields = ['nama', 'alamat', 'desa', 'kecamatan', 'kabupaten']
    ordering_fields = ['nama', 'jenis_fasilitas', 'level_fasilitas']
    ordering = ['nama']
    
    @action(detail=False, methods=['get'])
    def aktif(self, request):
        """Mengambil fasilitas kesehatan yang aktif."""
        queryset = self.queryset.filter(aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_pelayanan(self, request):
        """Mengambil fasilitas berdasarkan pelayanan."""
        pelayanan = request.query_params.get('pelayanan')
        if not pelayanan:
            return Response(
                {'error': 'pelayanan parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filter_kwargs = {f'pelayanan_{pelayanan}': True}
        queryset = self.queryset.filter(**filter_kwargs, aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik fasilitas kesehatan."""
        total_fasilitas = self.queryset.count()
        by_jenis = {}
        for choice in FasilitasKesehatan.JENIS_FASILITAS_CHOICES:
            by_jenis[choice[0]] = self.queryset.filter(jenis_fasilitas=choice[0]).count()
        
        by_level = {}
        for choice in FasilitasKesehatan.LEVEL_FASILITAS_CHOICES:
            by_level[choice[0]] = self.queryset.filter(level_fasilitas=choice[0]).count()
        
        by_pelayanan = {
            'anak': self.queryset.filter(pelayanan_anak=True).count(),
            'ibu_hamil': self.queryset.filter(pelayanan_ibu_hamil=True).count(),
            'imunisasi': self.queryset.filter(pelayanan_imunisasi=True).count(),
            'kb': self.queryset.filter(pelayanan_kb=True).count(),
            'gizi': self.queryset.filter(pelayanan_gizi=True).count(),
            'lab': self.queryset.filter(pelayanan_lab=True).count(),
            'radiologi': self.queryset.filter(pelayanan_radiologi=True).count(),
            'ugd': self.queryset.filter(pelayanan_ugd=True).count(),
        }
        
        return Response({
            'total_fasilitas': total_fasilitas,
            'by_jenis': by_jenis,
            'by_level': by_level,
            'by_pelayanan': by_pelayanan,
        })


class RujukanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Rujukan."""
    queryset = Rujukan.objects.all()
    serializer_class = RujukanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['pasien_id', 'posyandu_id', 'jenis_pasien', 'status', 'prioritas', 'tanggal_rujukan']
    search_fields = ['pasien_id', 'posyandu_id', 'alasan_rujukan', 'petugas_rujukan']
    ordering_fields = ['tanggal_rujukan', 'created_at']
    ordering = ['-tanggal_rujukan']
    
    @action(detail=False, methods=['get'])
    def by_pasien(self, request):
        """Mengambil rujukan berdasarkan pasien."""
        pasien_id = request.query_params.get('pasien_id')
        if not pasien_id:
            return Response(
                {'error': 'pasien_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(pasien_id=pasien_id)
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
    def statistics(self, request):
        """Statistik rujukan."""
        total_rujukan = self.queryset.count()
        by_status = {
            'dikirim': self.queryset.filter(status='dikirim').count(),
            'diterima': self.queryset.filter(status='diterima').count(),
            'dalam_proses': self.queryset.filter(status='dalam_proses').count(),
            'selesai': self.queryset.filter(status='selesai').count(),
            'ditolak': self.queryset.filter(status='ditolak').count(),
            'batal': self.queryset.filter(status='batal').count(),
        }
        by_prioritas = {
            'rendah': self.queryset.filter(prioritas='rendah').count(),
            'sedang': self.queryset.filter(prioritas='sedang').count(),
            'tinggi': self.queryset.filter(prioritas='tinggi').count(),
            'darurat': self.queryset.filter(prioritas='darurat').count(),
        }
        by_jenis_pasien = {
            'balita': self.queryset.filter(jenis_pasien='balita').count(),
            'ibu_hamil': self.queryset.filter(jenis_pasien='ibu_hamil').count(),
            'wus': self.queryset.filter(jenis_pasien='wus').count(),
        }
        
        return Response({
            'total_rujukan': total_rujukan,
            'by_status': by_status,
            'by_prioritas': by_prioritas,
            'by_jenis_pasien': by_jenis_pasien,
        })


class FollowUpRujukanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model FollowUpRujukan."""
    queryset = FollowUpRujukan.objects.all()
    serializer_class = FollowUpRujukanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rujukan', 'status', 'tanggal_follow_up']
    search_fields = ['rujukan__pasien_id', 'petugas_follow_up']
    ordering_fields = ['tanggal_follow_up', 'created_at']
    ordering = ['-tanggal_follow_up']
    
    @action(detail=False, methods=['get'])
    def by_rujukan(self, request):
        """Mengambil follow-up berdasarkan rujukan."""
        rujukan_id = request.query_params.get('rujukan_id')
        if not rujukan_id:
            return Response(
                {'error': 'rujukan_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(rujukan_id=rujukan_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Mengambil follow-up berdasarkan status."""
        status_follow_up = request.query_params.get('status')
        if not status_follow_up:
            return Response(
                {'error': 'status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(status=status_follow_up)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik follow-up rujukan."""
        total_follow_up = self.queryset.count()
        by_status = {
            'belum_datang': self.queryset.filter(status='belum_datang').count(),
            'sudah_datang': self.queryset.filter(status='sudah_datang').count(),
            'tidak_datang': self.queryset.filter(status='tidak_datang').count(),
            'reschedule': self.queryset.filter(status='reschedule').count(),
        }
        
        return Response({
            'total_follow_up': total_follow_up,
            'by_status': by_status,
        })


class TemplateRujukanViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model TemplateRujukan."""
    queryset = TemplateRujukan.objects.all()
    serializer_class = TemplateRujukanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['jenis_pasien', 'aktif']
    search_fields = ['nama_template', 'indikasi_rujukan']
    ordering_fields = ['nama_template', 'jenis_pasien']
    ordering = ['nama_template']
    
    @action(detail=False, methods=['get'])
    def aktif(self, request):
        """Mengambil template rujukan yang aktif."""
        queryset = self.queryset.filter(aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_jenis_pasien(self, request):
        """Mengambil template berdasarkan jenis pasien."""
        jenis_pasien = request.query_params.get('jenis_pasien')
        if not jenis_pasien:
            return Response(
                {'error': 'jenis_pasien parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(jenis_pasien=jenis_pasien, aktif=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistik template rujukan."""
        total_template = self.queryset.count()
        by_jenis_pasien = {
            'balita': self.queryset.filter(jenis_pasien='balita').count(),
            'ibu_hamil': self.queryset.filter(jenis_pasien='ibu_hamil').count(),
            'wus': self.queryset.filter(jenis_pasien='wus').count(),
        }
        by_status = {
            'aktif': self.queryset.filter(aktif=True).count(),
            'tidak_aktif': self.queryset.filter(aktif=False).count(),
        }
        
        return Response({
            'total_template': total_template,
            'by_jenis_pasien': by_jenis_pasien,
            'by_status': by_status,
        })
