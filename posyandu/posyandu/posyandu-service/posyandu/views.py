"""
Views untuk posyandu-service.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Posyandu
from .serializers import PosyanduSerializer


class PosyanduViewSet(viewsets.ModelViewSet):
    """ViewSet untuk model Posyandu."""
    queryset = Posyandu.objects.all()
    serializer_class = PosyanduSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Mencari posyandu berdasarkan nama."""
        query = request.query_params.get('q', '')
        if query:
            queryset = self.queryset.filter(nama__icontains=query)
        else:
            queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
