from django.views.generic import TemplateView
from rest_framework import views, serializers, status
from rest_framework.response import Response


class Index(TemplateView):
    template_name = 'index.html'


class EncuestasIndex(TemplateView):
    template_name = 'encuestas.html'


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
