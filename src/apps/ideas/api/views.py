from django.db.models import Prefetch
from rest_framework import viewsets

from apps.ideas.models import Idea, Resolve
from .serializers import IdeaSerializer


class IdeaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IdeaSerializer
    queryset = Idea.objects.prefetch_related(
        Prefetch('resolve_set', queryset=Resolve.objects.order_by('-created'))
    ).order_by('-created')
