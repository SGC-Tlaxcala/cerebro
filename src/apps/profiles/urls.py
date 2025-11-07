from django.urls import path

from .views import UserQuickCreateView


app_name = 'profiles'

urlpatterns = [
    path('users/quick-add/', UserQuickCreateView.as_view(), name='user-quick-add'),
]
