from rest_framework import serializers
from .models import Proceso, Tipo, Documento, Revision, Reporte

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = '__all__'

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    revisiones = RevisionSerializer(many=True, read_only=True, source='revision_set')
    tipo = TipoSerializer(read_only=True)
    proceso = ProcesoSerializer(read_only=True)

    class Meta:
        model = Documento
        fields = ('id', 'nombre', 'slug', 'ruta', 'proceso', 'tipo', 'lmd', 'aprobado', 'activo', 'texto_ayuda', 'autor', 'created', 'updated', 'revisiones')

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
