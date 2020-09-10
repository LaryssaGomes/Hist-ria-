from django.urls import path, include
from .views.restante_views import *
from .views.usuariocomum_views import *
# Criei outra importação, porque essa de cima não estava chamando a views pessoa.
from django.conf.urls.static import static  # Para poder acessar os arquivos dentro de static
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings

from usuario import urls

urlpatterns = [
    path('add_projetos/', add_projetos, name='add_projetos'),
    path('novosTiposDeDocumentos/', novosTiposDeDocumentos, name='novosTiposDeDocumentos'),
    path('edi_perfil/', edi_perfil, name='edi_perfil'),
    path('inicio_projeto/', inicio_projeto, name='inicio_projeto'),
    path('inicio', busca_comum, name='busca_comum'),
    path('inicio_projeto/ver_projetos/<int:id>/adicionarBolsista/<int:bolsistaid>/', add_bolsista, name='add_bolsista'),
    path('inicio_projeto/edi_projetos/<int:id>/', edi_projetos, name='edi_projetos'),
    path('inicio_projeto/ver_projetos/<int:id>/deletar_pedido/<int:id_notificacao>/', cancelar_pedido, name = 'cancelar_pedido'),
    path('inicio_projeto/ver_projetos/<int:id>/', ver_projetos, name='ver_projetos'),  # editado
    path('inicio_projeto/ver_projetos/<int:id>/submit', ver_projetos, name='ver_projetos'),
    path('inicio_projeto/ver_projetos/<int:id>/add_arquivo/', add_arquivo, name='add_arquivo'),
    path('arquivo/<int:id>', visualizacao_comum, name='visualizacao_comum,'),
    path('cadastro/', include(urls))
]