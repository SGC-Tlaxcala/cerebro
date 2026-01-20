from django.urls import path
from . import views

app_name = "pmml"

urlpatterns = [
    path("signup/", views.register, name="register"),
    path("verify/<uuid:token>/", views.verify, name="verify"),
    # Redirección de raíz de app a signup si se desea, o dejarlo así
    path("", views.register, name="index"),
]
