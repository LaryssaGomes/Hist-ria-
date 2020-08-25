
from django.shortcuts import render, get_object_or_404, redirect  # get_object_or_404 para pega o objeto com o id x
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # permitir acesso
from django.http import HttpResponse
from django.core.paginator import Paginator  # Para poder realizar a paginação
from django.contrib import messages
import usuario.templates

from .models import Projetos, Arquivo, ProjetosDosUsuarios, PalavrasChave, TiposDeDocumento
from . import urls
from .forms import (ProjetoForm,
                    ArquivoForm,
                    VideoForm,
                    DocumentoForm,
                    AudioForm,
                    FotosForm,
                    PatrimonioCulturaForm)

# Este próximo import vai importar modelos do app usuario.


from usuario.forms import UsuarioComumForm
from collections import Counter
from usuario.models import UsuarioComum

@login_required
def novosTiposDeDocumentos(request):
    selecionaGenerico = request.POST.get('selecionaGenerico')
    novoElemento = request.POST.get('novoElemento') 
    novoGenerico = request.POST.get('novoGenerico') 
    novoEspecifico = request.POST.get('novoEspecifico')
    if novoElemento  and selecionaGenerico  :
        TiposDeDocumento.objects.create(tdd_geral=selecionaGenerico, tdd_especifico=novoElemento)

    if novoGenerico  and novoEspecifico  :
        TiposDeDocumento.objects.create(tdd_geral=novoGenerico, tdd_especifico=novoEspecifico)
        TiposDeDocumento.objects.create(tdd_geral=novoGenerico)
        
    return redirect('/inicio_projeto/')

def salvandoArquivo(request, id, form_arq, categoriaDeDocumento):
    arquivo = form_arq.save()
    arquivo.arq_tdd_id = get_object_or_404(TiposDeDocumento, pk=categoriaDeDocumento)
    dia = request.POST.get('dia')
    mes = request.POST.get('mes')
    ano = request.POST.get('ano')
    if(dia=="00" and mes=="00" and ano=="00"):
        arquivo.arq_data = "Não Identificado"
    else:
        data = dia+"/"+mes+"/"+ano
        arquivo.arq_data = data
    arquivo.arq_data_de_registro = timezone.now()
    arquivo.arq_pro_id = get_object_or_404(Projetos, pk=id)  # Colocando a chave Estrangeira (Projeto)
    return(arquivo)

def salvandoPatrimonioCultural(arquivo, form_patrimonio):
    if form_patrimonio.is_valid():
        patrimonioCultura = form_patrimonio.save(commit=False)
        if patrimonioCultura.pc_oficio or patrimonioCultura.pc_expressao or patrimonioCultura.pc_lugares or patrimonioCultura.pc_celebracoes or patrimonioCultura.pc_edificacoes:
            patrimonioCultura.pc_arq = arquivo
            patrimonioCultura.save()
    

def salvandoPalavrasChave(arquivo, Palavras):
    for palavra in Palavras:
        PalavrasChave.objects.create(pc_arq=arquivo, pc_palavras_chaves=palavra)

@login_required
def add_arquivo(request, id):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            listas_categorias_reptidas = TiposDeDocumento.objects.all().values_list('tdd_geral', flat=True)
            listas_categorias = set(listas_categorias_reptidas)
            listas_tipos_de_arquivo = TiposDeDocumento.objects.all().order_by('tdd_especifico')
            form_patrimonio = PatrimonioCulturaForm(request.POST, request.FILES)
            form_arq = ArquivoForm(request.POST, request.FILES)
            form_video = VideoForm(request.POST, request.FILES)
            form_documento = DocumentoForm(request.POST, request.FILES)
            form_audio = AudioForm(request.POST, request.FILES)
            form_foto = FotosForm(request.POST, request.FILES)
            categoriaDeDocumento = request.POST.get('arq_documento_especifico')
            palavrasChaves = request.POST.get('PalavraChave') 
            Palavras = palavrasChaves.split(','); 
            # Sistema de bloqueio  
            tipoDeArquivo = request.POST.get('arq_tipo_de_formato') 
            
            if form_arq.is_valid() and len(Palavras) < 6 and form_video.is_valid() and tipoDeArquivo == 'Video':

                arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                video = form_video.save()
                video.vid_arq = arquivo
                video.save()
                salvandoPatrimonioCultural(arquivo, form_patrimonio)
                return redirect('/inicio_projeto/')  # rediredionando para lista

            elif form_arq.is_valid() and len(Palavras) < 6 and form_documento.is_valid() and (tipoDeArquivo=='Impresso' or tipoDeArquivo=='Manuscrito'):

                arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                documento = form_documento.save()
                documento.doc_arq = arquivo
                documento.save()
                salvandoPatrimonioCultural(arquivo, form_patrimonio)
                return redirect('/inicio_projeto/')

            elif form_arq.is_valid() and len(Palavras) < 6 and form_foto.is_valid() and (tipoDeArquivo =='Fotografia' or tipoDeArquivo =='Gravura' or tipoDeArquivo =='Mapa' or tipoDeArquivo =='Pintura'):

                arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                foto = form_foto.save()
                foto.fot_arq = arquivo
                foto.save()
                salvandoPatrimonioCultural(arquivo, form_patrimonio)
                return redirect('/inicio_projeto/')

            elif form_arq.is_valid() and len(Palavras) < 6 and form_audio.is_valid() and tipoDeArquivo =='Audio':

                arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                arquivo.save()
                salvandoPalavrasChave(arquivo, Palavras)
                audio = form_audio.save()
                audio.aud_arq = arquivo
                audio.save()
                salvandoPatrimonioCultural(arquivo, form_patrimonio)
                return redirect('/inicio_projeto/')
            else:
                messages.error(request, 'Erro ao salvar arquivo')
        else:
            form_arq = ArquivoForm()
            form_video = VideoForm()
            form_documento = DocumentoForm()
            form_audio = AudioForm()
            form_foto = FotosForm()
            form_patrimonio = PatrimonioCulturaForm()
            listas_categorias_reptidas = TiposDeDocumento.objects.all().values_list('tdd_geral', flat=True)
            listas_categorias = set(listas_categorias_reptidas)
            listas_tipos_de_arquivo = TiposDeDocumento.objects.all().order_by('tdd_especifico')
        return render(request, 'arquivos/add_arquivo.html', {'form_arq': form_arq,
                                                            'form_video': form_video,
                                                            'form_documento':form_documento,
                                                            'form_audio':form_audio,
                                                            'form_foto':form_foto,
                                                            'listas_categorias':listas_categorias,
                                                            'listas_tipos_de_arquivo': listas_tipos_de_arquivo,
                                                            'form_patrimonio':form_patrimonio,
                                                             },
                                                             )     



    
def busca_comum(request):
    arquivo = Arquivo.objects.filter(arq_nivel_de_acesso='PU')
    if arquivo.exists():
        return render(request, 'usuariocomum/busca.html', {'arquivos': arquivo})
    else: 
       
        return render(request, 'usuariocomum/busca.html', )
   
    
   

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



'''
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
'''
@login_required
def ver_projetos(request, id):
    projeto = get_object_or_404(Projetos, pk=id)  # Pega as informações do projeto que tem o id passando pela url.
    
    # Esse o id de projeto tem algum arquivo salvo mande para a variavel arquivos.
    arquivos = Arquivo.objects.filter(arq_pro_id=id)

    # Id do bolsista pesquisado
    # idDoBolsista = request.POST.get('id_bolsista')
    context = {
       'projeto': projeto
    }
    # Lista de bolsistas e pesquisadores do projeto
    
    listas = ProjetosDosUsuarios.objects.filter(pdu_projetos=projeto).values('pdu_usuarios')
    
    if len(listas) == 1:
        context['apenasUmUsuario'] = 1
    
    context['listaDeUsuarios'] =  get_object_or_404(UsuarioComum, pk__in=listas)
    

    '''
   # Nome pesquisador

    nome = request.GET.get('nomeDoBolsista')
    # Retorna a lista de bolsistas pesquisada
    context['lista_bolsista'] = listaDosBolsista(nome, request)

   # Se depois de manda a lista de usuarios o um dos bolsistas for selecionado
    if idDoBolsista :
        bolsistaAdd = get_object_or_404(Bolsista, pk=idDoBolsista)
      # Salve os dados na tabela projeto dos usuarios
        ProjetosDosUsuarios.objects.create(pdu_projetos=projeto, pdu_usuarios=bolsistaAdd)
   # Verifica se o projeto tem arquivos
   '''
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

                projetos_use = ProjetosDosUsuarios.objects.create(pdu_projetos=projetos, pdu_usuarios= UsuarioComum.objects.get(id=request.user.id))

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
    context = {
       'usuario': UsuarioComum.objects.get(id=request.user.id)
       }
    if len(projetos) > 0:
        context['list_projetos'] = Projetos.objects.filter(pk__in=projetos)
        return render(request, 'projetos/inicio_projetos.html', context)  # mando projetos e usuario para o html
    else:
         return render(request, 'projetos/inicio_projetos.html', context)

@login_required
def edi_perfil(request):
    usuario = UsuarioComum.objects.get(id=request.user.id)
    
    
    form = UsuarioForm(instance=usuario)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario.save()
            return redirect('/inicio_projeto/')
        else:
            return render(request,'usuario/perfil.html', {'form': form })
    else:
        return render(request,'usuario/perfil.html', {'form': form })

