from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.db.models import Prefetch, Q

from apps.docs.models import Documento, Proceso, Revision, Tipo
from .serializers import DocumentoSerializer, ProcesoSerializer, TipoSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DocumentoSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = (
            Documento.objects.filter(activo=True)
            .select_related("tipo", "proceso")
            .prefetch_related(
                Prefetch(
                    "revision_set", queryset=Revision.objects.order_by("-revision")
                )
            )
        )
        params = self.request.query_params
        if params.get("lmd") is not None:
            qs = qs.filter(lmd=params.get("lmd") in ("1", "true", "True"))
        if params.get("resultados") is not None:
            qs = qs.filter(resultados=params.get("resultados") in ("1", "true", "True"))
        if params.get("activo") is not None:
            qs = qs.filter(activo=params.get("activo") in ("1", "true", "True"))
        if params.get("tipo_id"):
            qs = qs.filter(tipo_id=params.get("tipo_id"))
        if params.get("proceso_id"):
            qs = qs.filter(proceso_id=params.get("proceso_id"))
        query = (params.get("q") or "").strip()
        if query:
            qs = qs.filter(
                Q(nombre__icontains=query)
                | Q(texto_ayuda__icontains=query)
                | Q(proceso__proceso__icontains=query)
                | Q(tipo__tipo__icontains=query)
            )
        return qs.order_by("proceso__proceso", "nombre")


class TipoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TipoSerializer
    permission_classes = (AllowAny,)
    queryset = Tipo.objects.all().order_by("tipo")


class ProcesoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProcesoSerializer
    permission_classes = (AllowAny,)
    queryset = Proceso.objects.all().order_by("proceso")
