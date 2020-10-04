from django.shortcuts import render, get_object_or_404, redirect  # get_object_or_404 para pega o objeto com o id x
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # permitir acesso
from django.http import HttpResponse
from django.core.paginator import Paginator  # Para poder realizar a paginação
from django.contrib import messages

from ..models import Projetos, Arquivo, ProjetosDosUsuarios, TiposDeDocumento, Notificacao, Audio, Fotos, Video, Documento, PatrimonioCultura
from usuario.forms import UsuarioForm
from collections import Counter
from .. import urls
from usuario.models import UsuarioComum
import usuario.templates
from ..forms import (ProjetoForm,
                    ArquivoForm,
                    VideoForm,
                    DocumentoForm,
                    AudioForm,
                    FotosForm,
                    PatrimonioCulturaForm)

# Verificando se tem notificação para o usuario logado
def Noti(request):
    
    lista_de_notificacao = Notificacao.objects.filter(noti_bolsista=request.user.id)
    sem = False
    if lista_de_notificacao.exists():
        return (lista_de_notificacao)
    else:
        return(sem)
#  Permitir que o usuario perquisador add um tipo de documento
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
    

@login_required
def add_arquivo(request, id):
    projeto_do_usuarios = ProjetosDosUsuarios.objects.filter(pdu_projetos=id)
    for projeto_do_usuario in projeto_do_usuarios:
        if projeto_do_usuario.pdu_usuarios.id == request.user.id:

            if str(request.user) != 'AnonymousUser':
                context = {}
                context['notificacoes'] = Noti(request)
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
                    palavrasChaves = request.POST.get('arq_palavras_chaves') 
                    Palavras = palavrasChaves.split(','); 
                    tipoDeArquivo = request.POST.get('arq_tipo_de_formato') 

                    if form_arq.is_valid() and len(Palavras) < 6 and form_video.is_valid() and tipoDeArquivo == 'Video':

                        arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                        arquivo.save()
                        video = form_video.save()
                        video.vid_arq = arquivo
                        video.save()
                        salvandoPatrimonioCultural(arquivo, form_patrimonio)
                        return redirect('/inicio_projeto/')  # rediredionando para lista

                    elif form_arq.is_valid() and len(Palavras) < 6 and form_documento.is_valid() and (tipoDeArquivo=='Impresso' or tipoDeArquivo=='Manuscrito'):

                        arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                        arquivo.save()
                        documento = form_documento.save()
                        documento.doc_arq = arquivo
                        documento.save()
                        salvandoPatrimonioCultural(arquivo, form_patrimonio)
                        return redirect('/inicio_projeto/')

                    elif form_arq.is_valid() and len(Palavras) < 6 and form_foto.is_valid() and (tipoDeArquivo =='Fotografia' or tipoDeArquivo =='Gravura' or tipoDeArquivo =='Mapa' or tipoDeArquivo =='Pintura'):

                        arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                        arquivo.save()
                        foto = form_foto.save()
                        foto.fot_arq = arquivo
                        foto.save()
                        salvandoPatrimonioCultural(arquivo, form_patrimonio)
                        return redirect('/inicio_projeto/')

                    elif form_arq.is_valid() and len(Palavras) < 6 and form_audio.is_valid() and tipoDeArquivo =='Audio':

                        arquivo = salvandoArquivo(request, id, form_arq, categoriaDeDocumento)
                        arquivo.save()
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
                return render(request, 'arquivos/add_arquivo.html',{'form_arq': form_arq,
                                                                    'form_video': form_video,
                                                                    'form_documento':form_documento,
                                                                    'form_audio':form_audio,
                                                                    'form_foto':form_foto,
                                                                    'listas_categorias':listas_categorias,
                                                                    'listas_tipos_de_arquivo': listas_tipos_de_arquivo,
                                                                    'form_patrimonio':form_patrimonio,
                                                                    },
                                                                    )     
# Editar projeto ,chama função de Noti
@login_required
def edi_projetos(request, id):
    #if urls.path.name == 'add_projetos':
    projeto_do_usuarios = ProjetosDosUsuarios.objects.filter(pdu_projetos=id)
    for projeto_do_usuario in projeto_do_usuarios:
        if projeto_do_usuario.pdu_usuarios.id == request.user.id:
            projeto = get_object_or_404(Projetos, pk=id)
            form = ProjetoForm(instance=projeto)  # Os dados de projeto para o form
            editado = True
            context = {
                'form_pro': form,
                'edi': editado
            }
            context['notificacoes'] = Noti(request)
            if request.method == 'POST':  # Verificando se tem dados
                form = ProjetoForm(request.POST, request.FILES, instance=projeto)  # Passando esses dados para form
                if form.is_valid():  # Verificando se ta tudo preenchido
                    projeto.save()
                    return redirect('/inicio_projeto/')
                else:
                    return render(request, 'projetos/add_projetos.html', context)
            else:
                return render(request, 'projetos/add_projetos.html', context)



# lista os bolsistas em ver projeto
def listaDosBolsista(request, lista, id):

    # Pesquise os bolsistas com esse nome
    lista = UsuarioComum.objects.filter(tipo_de_usuario='BO').exclude(pk__in=lista)
    lista_de_notificacao = Notificacao.objects.filter(noti_arquivo=id).values('noti_bolsista')
    if lista_de_notificacao.exists():
        lista = lista.exclude(pk__in=lista_de_notificacao)
    # Se tiver algum bolsista com esse nome
    if len(lista) > 0:
        paginator = Paginator(lista, 3)
        page = request.GET.get('page')
        list_bolsista = paginator.get_page(page)
        
        return list_bolsista
    else:
        return False
       

'''
    Verificando se o usuario Bolsista logado tem alguma notificação
'''

@login_required
def add_bolsista(request,bolsistaid, id):
    Notificacao.objects.create(noti_bolsista = UsuarioComum.objects.get(id=bolsistaid), noti_pesquisador = UsuarioComum.objects.get(id=request.user.id),noti_arquivo= get_object_or_404(Projetos, pk=id))
    return redirect('ver_projetos',id=id)

def pedidos_pendentos(request, projetos):
    notificacoes_pendentes = Notificacao.objects.filter(noti_arquivo=projetos)
    return (notificacoes_pendentes)

@login_required
def ver_projetos(request, id):
    projeto_do_usuarios = ProjetosDosUsuarios.objects.filter(pdu_projetos=id)
    for projeto_do_usuario in projeto_do_usuarios:
        if projeto_do_usuario.pdu_usuarios.id == request.user.id:
            projeto = get_object_or_404(Projetos, pk=id)  # Pega as informações do projeto que tem o id passando pela url.
            # Esse o id de projeto tem algum arquivo salvo mande para a variavel arquivos.
            arquivos = Arquivo.objects.filter(arq_pro_id=id)
            # Id do bolsista pesquisado
            context = {
            'projeto': projeto
            }
            context['pendentes'] = pedidos_pendentos(request, projeto)
            # Lista de bolsistas e pesquisadores do projeto
            
            listas = ProjetosDosUsuarios.objects.filter(pdu_projetos=projeto).values('pdu_usuarios')
            
            if len(listas) == 1:
                context['apenasUmUsuario'] = 1
            else:
                context['listaDeUsuarios'] =  UsuarioComum.objects.filter(pk__in=listas)
                
        # Nome pesquisador

            # Retorna a lista de bolsistas pesquisada
            context['lista_bolsista'] = listaDosBolsista(request, listas, id)
            context['notificacoes'] = Noti(request)
            aceito = request.POST.get('button_aceito') 
            recusado = request.POST.get('button_recusado')
            
            if aceito or recusado:
                aceito_projeto(aceito, request, recusado)
        # Verifica se o projeto tem arquivos
        
            if len(arquivos) > 0:
                context['list_arquivos'] = arquivos
                return render(request, 'projetos/ver_projetos.html', context)
            else:
                return render(request, 'projetos/ver_projetos.html', context)


@login_required
def add_projetos(request):
    aceito = request.POST.get('button_aceito') 
    recusado = request.POST.get('button_recusado')
    
    if aceito or recusado:
       aceito_projeto(aceito, request, recusado)
    
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
            context ={
                'form_pro':ProjetoForm()
            }
            context['notificacoes'] = Noti(request)

        return render(request, 'projetos/add_projetos.html', context)
    else:
        return redirect('/')

def aceito_projeto(aceito, request, recusado):
    
    if aceito:
        notificacao = Notificacao.objects.get(id=aceito)
        ProjetosDosUsuarios.objects.create(pdu_projetos=notificacao.noti_arquivo, pdu_usuarios= UsuarioComum.objects.get(id=request.user.id))
        notificacao.delete()
    if recusado:
        notificacao = get_object_or_404(Notificacao, id=recusado)
        notificacao.delete()
        


@login_required
def inicio_projeto(request):
# Verifica se o usuario tem algum projeto
    projetos = ProjetosDosUsuarios.objects.filter(pdu_usuarios=request.user).values('pdu_projetos')
    context = {
       'usuario': UsuarioComum.objects.get(id=request.user.id)
       }
    context['notificacoes'] = Noti(request)  # Verificando se tem notificações
    aceito = request.POST.get('button_aceito') 
    recusado = request.POST.get('button_recusado')
    
    if aceito or recusado:
       aceito_projeto(aceito, request, recusado)
       
    if projetos.exists():
      
        context['list_projetos'] = Projetos.objects.filter(pk__in=projetos)
    
    return render(request, 'projetos/inicio_projetos.html', context)

@login_required
def cancelar_pedido(request, id_notificacao, id):
    pedido = get_object_or_404( Notificacao, pk=id_notificacao)
    pedido.delete()
    return redirect ('ver_projetos',id)

@login_required
def edi_perfil(request):
    usuario = UsuarioComum.objects.get(id=request.user.id)
    form = UsuarioForm(instance=usuario)
    context ={
        'form': form
    }
    context['notificacoes'] = Noti(request)
    aceito = request.POST.get('button_aceito') 
    recusado = request.POST.get('button_recusado')
    
    if aceito or recusado:
       aceito_projeto(aceito, request, recusado)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario.save()
            return redirect('/inicio_projeto/')
        else:
            return render(request,'usuario/perfil.html', context)
    else:
        return render(request,'usuario/perfil.html', context)
# Tipo de documento
def edi_arquivo(request, id_arquivo, id):
    projeto_do_usuarios = ProjetosDosUsuarios.objects.filter(pdu_projetos=id)
    for projeto_do_usuario in projeto_do_usuarios:
        if projeto_do_usuario.pdu_usuarios.id == request.user.id:
            arquivo = get_object_or_404(Arquivo, pk=id_arquivo)
            tipo_do_documento = arquivo.arq_tdd_id
            form_arq = ArquivoForm(instance=arquivo)
            listas_categorias_reptidas = TiposDeDocumento.objects.all().values_list('tdd_geral', flat=True)
            listas_categorias = set(listas_categorias_reptidas)
            listas_tipos_de_arquivo = TiposDeDocumento.objects.all().order_by('tdd_especifico')
            

            context ={
                'form_arq': form_arq,
                'listas_categoria': listas_categorias,
                'listas_tipos_de_arquivo': listas_tipos_de_arquivo,
                'tipo_do_documento':tipo_do_documento,
            }
           
            patrimonio_cultura = PatrimonioCultura.objects.filter(pc_arq=id_arquivo).first()
            palavras_chaves = request.POST.get('arq_palavras_chaves') 
            if palavras_chaves:
                palavras = palavras_chaves.split(','); 
            if patrimonio_cultura:
                if request.method == 'POST' and len(palavras)<6:
                    form_patrimonio_cultura = PatrimonioCulturaForm(request.POST, request.FILES, instance=patrimonio_cultura)
                    if form_patrimonio_cultura.is_valid():
                        patrimonio_cultura.save()
                form_patrimonio_cultura =  PatrimonioCulturaForm(instance=patrimonio_cultura)
                context['form_patrimonio_cultura'] = form_patrimonio_cultura
            else:
                if request.method == 'POST' and len(palavras)<6:
                    form_patrimonio_cultura =  PatrimonioCulturaForm(request.POST, request.FILES)
                    if form_patrimonio_cultura.is_valid():
                        patrimonio_cultura = form_patrimonio_cultura.save()
                        patrimonio_cultura.pc_arq = arquivo
                        patrimonio_cultura.save() 
                else:
                    context['form_patrimonio_cultura'] = PatrimonioCulturaForm()
                
            documento = Documento.objects.filter(doc_arq=id_arquivo).first()
            if documento:  
                if request.method == 'POST' and len(palavras)<6:
                    categoriaDeDocumento = request.POST.get('arq_documento_especifico')
                    form_arq = ArquivoForm(request.POST, request.FILES, instance=arquivo)
                    form_documento = DocumentoForm(request.POST, request.FILES, instance=documento)
                    if form_documento.is_valid() and form_arq.is_valid():
                        arquivo = form_arq
                        print(categoriaDeDocumento)
                        arquivo.arq_tdd_id = get_object_or_404(TiposDeDocumento, pk=categoriaDeDocumento)
                        arquivo.save()
                        documento_arq = form_documento
                        documento_arq.save()
                        return redirect('/inicio_projeto/')
                form_documento = DocumentoForm(instance=documento)
                context['form'] = form_documento
                return render(request, 'arquivos/adi_arquivo.html',context)
            foto = Fotos.objects.filter(fot_arq=id_arquivo).first()
            if foto:
                if request.method == 'POST' and len(palavras)<6:
                    categoriaDeDocumento = request.POST.get('arq_documento_especifico')
                    form_arq = ArquivoForm(request.POST, request.FILES, instance=arquivo)
                    form = FotosForm(request.POST, request.FILES, instance=foto)
                    if form.is_valid() and form_arq.is_valid():
                        arquivo = form_arq.save(commit=False)
                        arquivo.arq_tdd_id = get_object_or_404(TiposDeDocumento, pk=categoriaDeDocumento)
                        arquivo.save()
                        foto_arq = form.save(commit=False)
                        foto_arq.save()
                        return redirect('/inicio_projeto/')
                form_foto = FotosForm(instance=foto)
                context['form'] = form_foto
                return render(request, 'arquivos/adi_arquivo.html',context)
            video = Video.objects.filter(vid_arq=id_arquivo).first()
            if video:

                if request.method == 'POST' and len(palavras)<6:
                    categoriaDeDocumento = request.POST.get('arq_documento_especifico')
                    form_arq = ArquivoForm(request.POST, request.FILES, instance=arquivo)
                    form = VideoForm(request.POST, request.FILES, instance=video)
                    if form.is_valid() and form_arq.is_valid():
                        arquivo = form_arq.save(commit=False)
                        arquivo.arq_tdd_id = get_object_or_404(TiposDeDocumento, pk=categoriaDeDocumento)
                        arquivo.save()
                        video_arq = form.save(commit=False)
                        video_arq.save()
                        return redirect('/inicio_projeto/')
                form_video = VideoForm(instance=video)
                context['form'] = form_video
                return render(request, 'arquivos/adi_arquivo.html',context)
            else:
                audio = Audio.objects.filter(aud_arq=id_arquivo).first()
                if request.method == 'POST' and len(palavras)<6:
                    categoriaDeDocumento = request.POST.get('arq_documento_especifico')
                    form_arq = ArquivoForm(request.POST, request.FILES, instance=arquivo)
                    form = AudioForm(request.POST, request.FILES, instance=audio)
                    if form.is_valid() and form_arq.is_valid():
                        arquivo = form_arq.save(commit=False)
                        arquivo.arq_tdd_id = get_object_or_404(TiposDeDocumento, pk=categoriaDeDocumento)
                        arquivo.save()
                        audio_arq = form.save(commit=False)
                        audio_arq.save()
                        return redirect('/inicio_projeto/')
                form_audio = VideoForm(instance=audio)
                context['form'] = form_audio
                return render(request, 'arquivos/adi_arquivo.html',context)