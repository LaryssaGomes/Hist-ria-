from django.urls import path, include
from . import views
# Criei outra importação, porque essa de cima não estava chamando a views pessoa.
from django.conf.urls.static import static  # para poder acessar os arquivos dentro de static
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings

from usuario import urls

urlpatterns = [
    path('add_projetos/', views.add_projetos, name='add_projetos'),
    path('novosTiposDeDocumentos/', views.novosTiposDeDocumentos, name='novosTiposDeDocumentos'),
    path('edi_perfil/', views.edi_perfil, name='edi_perfil'),
    path('inicio_projeto/', views.inicio_projeto, name='inicio_projeto'),
    path('inicio', views.busca_comum, name='busca_comum'),
    path('inicio_projeto/edi_projetos/<int:id>/', views.edi_projetos, name='/edi_projetos'),
    path('inicio_projeto/ver_projetos/<int:id>/', views.ver_projetos, name='ver_projetos'),  # editado
    path('inicio_projeto/ver_projetos/<int:id>/submit', views.ver_projetos, name='ver_projetos'),
    path('inicio_projeto/ver_projetos/<int:id>/add_arquivo/', views.add_arquivo, name='add_arquivo'),
    path('arquivo/<int:id>', views.visualizacao_comum, name='visualizacao_comum,'),
    path('cadastro/', include(urls))
]
