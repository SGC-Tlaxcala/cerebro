from rest_framework import serializers

from apps.docs.models import Documento, Proceso, Tipo


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = ['id', 'tipo', 'slug']


class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = ['id', 'proceso', 'slug']


class DocumentoSerializer(serializers.ModelSerializer):
    clave = serializers.SerializerMethodField()
    tipo = TipoSerializer(read_only=True)
    proceso = ProcesoSerializer(read_only=True)
    detail_url = serializers.SerializerMethodField()
    revision = serializers.SerializerMethodField()

    class Meta:
        model = Documento
        fields = [
            'id',
            'nombre',
            'slug',
            'clave',
            'ruta',
            'lmd',
            'resultados',
            'activo',
            'texto_ayuda',
            'tipo',
            'proceso',
            'detail_url',
            'revision',
            'created',
            'updated',
        ]

    def get_clave(self, obj):
        return obj.clave()

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.get_absolute_url()) if hasattr(obj, 'get_absolute_url') else None
        return None

    def get_revision(self, obj):
        rev = obj.revision_set.order_by('-revision').first()
        if not rev:
            return None
        return {
            'numero': rev.revision,
            'fecha': rev.f_actualizacion,
            'archivo': rev.archivo.url if rev.archivo else None,
        }
