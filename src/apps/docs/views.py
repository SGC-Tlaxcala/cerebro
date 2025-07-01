"""
Vistas para la app docs.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Documento, Proceso, Reporte, Revision, Tipo
from .serializers import (DocumentoSerializer, ProcesoSerializer, ReporteSerializer,
                          RevisionSerializer, TipoSerializer)


class ProcesoViewSet(viewsets.ModelViewSet):
    queryset = Proceso.objects.all()
    serializer_class = ProcesoSerializer
    permission_classes = [IsAuthenticated]


class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    permission_classes = [IsAuthenticated]


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]


class RevisionViewSet(viewsets.ModelViewSet):
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer
    permission_classes = [IsAuthenticated]


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]
