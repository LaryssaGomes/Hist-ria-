from django.urls import path
from .views import usuario, validar_email_usuario


urlpatterns = [
    path('usuario/', usuario, name='usuario'),
    path('validar_email_usuario/', validar_email_usuario, name='validar_email_usuario')
]
