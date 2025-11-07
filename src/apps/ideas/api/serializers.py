from rest_framework import serializers

from apps.ideas.models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    scope_display = serializers.CharField(source='get_scope_display', read_only=True)
    latest_resolution = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = [
            'id',
            'title',
            'slug',
            'type',
            'type_display',
            'scope',
            'scope_display',
            'name',
            'contact',
            'site',
            'desc',
            'results',
            'created',
            'latest_resolution',
        ]

    def get_latest_resolution(self, obj):
        resolution = obj.latest_resolution
        if not resolution:
            return None
        return {
            'viable': resolution.viable,
            'resolve': resolution.resolve,
            'created': resolution.created,
        }
