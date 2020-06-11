""" Arquivo das funcionalidades da aplicação. Serão chamadas pelas urls.
# Conecta models.py com os templates
"""
from django.shortcuts import render, get_object_or_404, redirect  # get_object_or_404 para pega o objeto com o id x
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # permitir acesso
from django.http import HttpResponse
from django.core.paginator import Paginator  # Para poder realizar a paginação
from django.contrib import messages
import usuario.templates

from .models import Projetos, Arquivo, ProjetosDosUsuarios
from . import urls
from .forms import (ProjetoForm,
                    ArquivoForm)

# Este próximo import vai importar modelos do app usuario.
from usuario.models import Pessoa, Pesquisador, Bolsista
'''
    Corrigir a paginação, de ver projetos e de visualização comum
'''
@login_required
def add_arquivo(request, id):
    if str(request.user) != 'AnonymousUser':

        if str(request.method) == "POST":
            form_arq = ArquivoForm(request.POST, request.FILES)
            if form_arq.is_valid():
                arquivo = form_arq.save()
                arquivo.arq_usu_id = request.user  # Colocando a chava Estrangeira (Usuario)
                arquivo.arq_pro_id = get_object_or_404(Projetos, pk=id)  # Colocando a chave Estrangeira (Projeto)
                arquivo.save()
                return redirect('/inicio_projeto/')  # rediredionando para lista
        else:
            form_arq = ArquivoForm()
        return render(request, 'arquivos/add_arquivo.html', {'form_arq': form_arq})
    else:
        return redirect('/')
    

def busca_comum(request):
    search = request.GET.get('search')  # Pegando o dado pela url
    
    if search:  # vai ser executado quando eu enviar as informações
        # problema não consigo manda os dois elementos na url,logo so consigo executar um por fez.

        """
        Aqui estou realizando a busca se nos projetos tem algo com um titulo
        parecido com o que foi pego na url.  
        """
        arquivos = Arquivo.objects.filter(arq_nome=search)
        paginador = Paginator(arquivos, 3)  # De projetos eu pego 3 elementos
        page = request.GET.get('page')  # Mando pela url o numero da pagina que eu estou
        arquivos = paginador.get_page(page)  # Pego esse numero
        
    else: 
        return render(request, 'usuariocomum/busca.html')
       
    return render(request, 'usuariocomum/busca.html', {'arquivos': arquivos})


def visualizacao_comum(request, id):  # Da uma olhada nesse argumento 'id' depois
    arquivos = get_object_or_404(Arquivo, pk=id)  # Pegando todos os dados na linha que tem o id passado na url.
    return render(request, 'usuariocomum/resultado_busca.html', {'arquivos': arquivos})


@login_required
def edi_projetos(request, id):
    if urls.path.name == 'add_projetos':
        print('Você esta adicionando um projeto agora')
    projeto = get_object_or_404(Projetos, pk=id)
    form = ProjetoForm(instance=projeto)  # Os dados de projeto para o form
    if request.method == 'POST':  # Verificando se tem dados
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)  # Passando esses dados para form
        if form.is_valid():  # Verificando se ta tudo preenchido
            projeto.save()
            return redirect('/inicio_projeto/')
        else:
            return render(request, 'projetos/edi_projetos.html', {'form': form, 'projeto': projeto})
    else:
        return render(request, 'projetos/edi_projetos.html', {'form': form, 'projeto': projeto})



def listaDosUsuarios(projeto):
    listas = ProjetosDosUsuarios.objects.filter(pdu_projetos=projeto)

    for usuario in listas:
        qualEPesquisador = Pesquisador.objects.filter(id=usuario.pdu_usuarios.id)
        if(qualEPesquisador):
            Pesquisa = usuario.pdu_usuarios
            return(listas, Pesquisa)

def listaDosBolsista(nome, request):
    
    if nome :
        # Pesquise os bolsistas com esse nome
        lista = Bolsista.objects.filter(nome__icontains=nome)
        
        # Se tiver algum bolsista com esse nome
        if len(lista) > 0:
            paginator = Paginator(lista, 3)
            page = request.GET.get('page')
            list_bolsista = paginator.get_page(page)
            # Mande a lista desses bolsistas
            return list_bolsista
    
@login_required
def ver_projetos(request, id):
    projeto = get_object_or_404(Projetos, pk=id)  # Pega as informações do projeto que tem o id passando pela url.
    # Esse o id de projeto tem algum arquivo salvo mande para a variavel arquivos.
    arquivos = Arquivo.objects.filter(arq_pro_id=id)
    
    
    # Id do bolsista pesquisado
    idDoBolsista = request.POST.get('id_bolsista') 
    context = {
        'projeto': projeto 
    }
    # Lista de bolsistas e pesquisadores do projeto
    context['lista'] ,context['Pesquisador'] = listaDosUsuarios(projeto) 
    # Nome pesquisador 
    
    nome = request.POST.get('nomeDoBolsista') 
    # Retorna a lista de bolsistas pesquisada
    
    context['lista_bolsista'] = listaDosBolsista(nome, request)
    
    # Se depois de manda a lista de usuarios o um dos bolsistas for selecionado
    if idDoBolsista :
        # Pega os dados desse bolsista
        bolsistaAdd = get_object_or_404(Bolsista, pk=idDoBolsista)
        # Salve os dados na tabela projeto dos usuarios
        ProjetosDosUsuarios.objects.create(pdu_projetos=projeto, pdu_usuarios=bolsistaAdd)
    # Verifica se o projeto tem arquivos
    if len(arquivos) > 0: 
        context['list_arquivos'] = arquivos
        return render(request, 'projetos/ver_projetos.html', context) 
    else:
        return render(request, 'projetos/ver_projetos.html', context)


@login_required
def add_projetos(request):
    
    if str(request.user) != 'AnonymousUser':

        if str(request.method) == "POST":
            form_pro = ProjetoForm(request.POST, request.FILES)
            if form_pro.is_valid():
                form_pro.save()
                projetos = form_pro.save()
                projetos.pro_datetime = timezone.now()
                projetos.save()
                # salvando dos forenkey
                projetos_use = ProjetosDosUsuarios.objects.create(pdu_projetos=projetos, pdu_usuarios=request.user)
                return redirect('/inicio_projeto/')  # rediredionando para lista
        else:
            form_pro = ProjetoForm()
        return render(request, 'projetos/add_projetos.html', {'form_pro': form_pro})
    else:
        return redirect('/')


@login_required
def inicio_projeto(request):
    # Verifica se o usuario tem algum projeto
    projetos = ProjetosDosUsuarios.objects.filter(pdu_usuarios=request.user)
    pesquisador = Pesquisador.objects.filter(id=request.user.id)

    if len(pesquisador) > 0:
        context = {
            'usuario': Pesquisador.objects.get(id=request.user.id)
        }
        context['bolsistaOuPesquisador'] = 'Pesquisador'
    else:
        context = {
            'usuario': Bolsista.objects.get(id=request.user.id)
        }
        context['bolsistaOuPesquisador'] = 'Bolsista'
    if len(projetos) > 0:
        # verifico se tem informação em projetos,se tiver informação eu entro no if e faço o seguinte comando.
        context['list_projetos'] = Projetos.objects.filter(pk__in=projetos)
        return render(request, 'projetos/inicio_projetos.html', context)  # mando projetos e usuario para o html
    else:
        return render(request, 'projetos/inicio_projetos.html', context)


    
