from django.urls import path
from .views import pesquisador, bolsista


urlpatterns = [
    path('pesquisador/', pesquisador, name='pesquisador'),
    path('bolsista/', bolsista, name='bolsista')
]
