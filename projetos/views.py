"""
    Telas editadas
        add_arquivo.js
        busca.js
        busca.html
"""
from django.shortcuts import render, get_object_or_404, redirect  # get_object_or_404 para pega o objeto com o id x
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # permitir acesso
from django.http import HttpResponse
from django.core.paginator import Paginator  # Para poder realizar a paginação
from django.contrib import messages
import usuario.templates

from .models import Projetos, Arquivo, ProjetosDosUsuarios, PalavrasChave
from . import urls
from .forms import (ProjetoForm,
                    ArquivoForm,
                    VideoForm,
                    DocumentoForm,
                    AudioForm,
                    FotosForm)

# Este próximo import vai importar modelos do app usuario.
from usuario.models import Pessoa, Pesquisador, Bolsista
from usuario.forms import Bolsista1Form, Pesquisador1Form
from collections import Counter


def salvandoArquivo(request, id, form_arq, estado, cidade):
    arquivo = form_arq.save()
    textoNao = request.POST.get('opcao')
    if arquivo.arq_texto and textoNao == 0:
        arquivo.arq_texto = ' '
    dia = request.POST.get('dia')
    mes = request.POST.get('mes')
    ano = request.POST.get('ano')
    if(dia=="00" and mes=="00" and ano=="00"):
        arquivo.arq_data = "Não Identificado"
    else:
        data = dia+"/"+mes+"/"+ano
        arquivo.arq_data = data
    
    arquivo.arq_estado = estado
    arquivo.arq_cidade = cidade
    arquivo.arq_data_de_registro = timezone.now()
    arquivo.arq_usu_id = request.user  # Colocando a chava Estrangeira (Usuario)
    arquivo.arq_pro_id = get_object_or_404(Projetos, pk=id)  # Colocando a chave Estrangeira (Projeto)
    return(arquivo)

def testando(request):
    search = request.GET.get('search')
    if search:
        search = search.lower()  
        palavrasBuscadas = search.split(' ')
        encontrado = PalavrasChave.objects.filter(pc_palavras_chaves__in=palavrasBuscadas).values_list('pc_arq',flat=True)
        arquivo = Arquivo.objects.filter(pk__in=encontrado, arq_nivel_de_acesso='PU')
        context={}
        context['person_list'] = arquivo
        return render(request, 'arquivos/index.html', context)
    else:
        return render(request, 'arquivos/index.html')

def salvandoPalavrasChave(arquivo, Palavras):
    for palavra in Palavras:
        PalavrasChave.objects.create(pc_arq=arquivo, pc_palavras_chaves=palavra)

@login_required
def add_arquivo(request, id):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            
            form_arq = ArquivoForm(request.POST, request.FILES)
            form_video = VideoForm(request.POST, request.FILES)
            form_documento = DocumentoForm(request.POST, request.FILES)
            form_audio = AudioForm(request.POST, request.FILES)
            form_foto = FotosForm(request.POST, request.FILES)
            estado = request.POST.get('estado') 
            cidade = request.POST.get('cidade')
            palavrasChaves = request.POST.get('PalavraChave') 
            Palavras = palavrasChaves.split(); 
            # Sistema de bloqueio  
            tipoDeArquivo = request.POST.get('tipoDeDocumento')  
            if form_arq.is_valid() and len(Palavras) < 6 and form_video.is_valid() and tipoDeArquivo == 'V':

                arquivo = salvandoArquivo(request, id, form_arq, estado, cidade)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                video = form_video.save()
                video.vid_arq = arquivo
                video.save()
                
                return redirect('/inicio_projeto/')  # rediredionando para lista

            elif form_arq.is_valid() and len(Palavras) < 6 and form_documento.is_valid() and tipoDeArquivo =='D':

                arquivo = salvandoArquivo(request, id, form_arq, estado, cidade)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                documento = form_documento.save()
                documento.doc_arq = arquivo
                documento.save()
                return redirect('/inicio_projeto/')

            elif form_arq.is_valid() and len(Palavras) < 6 and form_foto.is_valid() and tipoDeArquivo =='F':

                arquivo = salvandoArquivo(request, id, form_arq, estado, cidade)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                foto = form_foto.save()
                foto.fot_arq = arquivo
                foto.save()
                return redirect('/inicio_projeto/')

            elif form_arq.is_valid() and len(Palavras) < 6 and form_audio.is_valid() and tipoDeArquivo =='A':

                arquivo = salvandoArquivo(request, id, form_arq, estado, cidade)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                audio = form_audio.save()
                audio.aud_arq = arquivo
                audio.save()
                return redirect('/inicio_projeto/')
            else:
                messages.error(request, 'Erro ao salvar arquivo')
        else:
            form_arq = ArquivoForm()
            form_video = VideoForm()
            form_documento = DocumentoForm()
            form_audio = AudioForm()
            form_foto = FotosForm()
        return render(request, 'arquivos/add_arquivo.html', {'form_arq': form_arq,
                                                             'form_video': form_video,
                                                             'form_documento':form_documento,
                                                             'form_audio':form_audio,
                                                             'form_foto':form_foto,},
                                                             )      
    


def busca_comum(request):
    search = request.GET.get('search') 
    estado = request.GET.get('estado')
    cidade = request.GET.get('cidade')
    # Tipo de documento 
    # Ano do documento
    
    if search:
        search = search.lower()  
        palavrasBuscadas = search.split(' ')
        encontrado = PalavrasChave.objects.filter(pc_palavras_chaves__in=palavrasBuscadas).values_list('pc_arq',flat=True)
        arquivo = Arquivo.objects.filter(pk__in=encontrado, arq_nivel_de_acesso='PU')
        if estado:
            arquivo = arquivo.filter(arq_estado=estado)
            if cidade:
                arquivo = arquivo.filter(arq_cidade=cidade)
    else: 
        return render(request, 'usuariocomum/busca.html')
   
    return render(request, 'usuariocomum/busca.html', {'arquivos': arquivo,'search':search})
   

def visualizacao_comum(request, id):  # Da uma olhada nesse argumento 'id' depois
    arquivos = get_object_or_404(Arquivo, pk=id)  # Pegando todos os dados na linha que tem o id passado na url.
    return render(request, 'usuariocomum/resultado_busca.html', {'arquivos': arquivos})


@login_required
def edi_projetos(request, id):
    #if urls.path.name == 'add_projetos':
    #    print('Você esta adicionando um projeto agora')
    projeto = get_object_or_404(Projetos, pk=id)
    form = ProjetoForm(instance=projeto)  # Os dados de projeto para o form
    if request.method == 'POST':  # Verificando se tem dados
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)  # Passando esses dados para form
        if form.is_valid():  # Verificando se ta tudo preenchido
            projeto.save()
            return redirect('/inicio_projeto/')
        else:
            return render(request, 'projetos/edi_projetos.html', {'form': form })
    else:
        return render(request, 'projetos/edi_projetos.html', {'form': form })



def listaDosUsuarios(projeto):
    listas = ProjetosDosUsuarios.objects.filter(pdu_projetos=projeto)
    
    if len(listas) != 0:
        for usuario in listas:
            qualEPesquisador = Pesquisador.objects.filter(id=usuario.pdu_usuarios.id)
            if(qualEPesquisador):
                Pesquisa = usuario.pdu_usuarios
                return(listas, Pesquisa)
    else:
        
        Pesquisa = 1
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
    
    nome = request.GET.get('nomeDoBolsista') 
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


@login_required
def edi_perfil(request):
    pesquisador = Pesquisador.objects.filter(id=request.user.id)

    if len(pesquisador) > 0:
        pesquisado = Pesquisador.objects.get(id=request.user.id)
        form = Pesquisador1Form(instance=pesquisado)
        if request.method == 'POST':  
            form = Pesquisador1Form(request.POST, request.FILES, instance=pesquisado)  
            if form.is_valid():  
                pesquisado.save()
                return redirect('/inicio_projeto/')
            else:
                return render(request,'usuario/perfil.html', {'form': form, 'pesquisado': pesquisado })
        else:
            return render(request,'usuario/perfil.html', {'form': form, 'pesquisado': pesquisado } )
    else:
        bolsista = Bolsista.objects.get(id=request.user.id)
        form = Bolsista1Form(instance=bolsista)
        if request.method == 'POST':  
            form = Bolsista1Form(request.POST, request.FILES, instance=bolsista)  
            if form.is_valid():  
                bolsista.save()
                return redirect('/inicio_projeto/')
            else:
                return render(request,'usuario/perfil.html', {'form': form, 'pesquisado': bolsista })
        else:
            return render(request,'usuario/perfil.html', {'form': form, 'pesquisado': bolsista } )