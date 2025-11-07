from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import BasePermission

from .serializers import UserProfileSerializer


User = get_user_model()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserProfileSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSuperUser,)
