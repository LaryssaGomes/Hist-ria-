from django.shortcuts import render, get_object_or_404
from .forms import UsuarioComumForm, ValidarCadastroUsuario
from django.contrib import messages
from .models import UsuarioComum, Instituicoes
from .forms import sequencia
from usuario.funcoes_suporte import cpf
from django.contrib.auth.models import Group


def usuario(request):
    """
    # View do pesquisador, responsável por verificar se o formulario está vazio
    # ou não, validar os dados e salvar no banco.
    """

    if str(request.method) == 'POST':  # Verifica se é o formulário ja tem dados a serem submetidos.
        form = UsuarioComumForm(request.POST, request.FILES)
        instituicoes = Instituicoes.objects.all()
        instituicao_id = request.POST.get('nome_instituicao')
        # print(f'olha aqui!!! {instituicao_id}')
        # new_form = form.save(commit=False)
        if form.is_valid():
            valida_cpf = form.save(commit=False)

            if cpf.isCpfValid(valida_cpf.cpf):
                user = form.save(commit=False)
                user.salvar_instituicao = instituicao_id
                user.username = form.cleaned_data['email']
                codigo_refatorado = ' '.join(map(str, sequencia()))
                user.codigo = codigo_refatorado

                if user.tipo_de_usuario == 'PE':
                    tipo = 'Pesquisador'
                elif user.tipo_de_usuario == 'BO':
                    tipo = 'Bolsista'

                grupo = get_object_or_404(Group, name=tipo)

                # user.object.groups.add(grupo)
                # user.object.save()
                print(user.email)

                form.save()  # Salva os dados
                rota_do_usuario = get_object_or_404(UsuarioComum, email=user.email)
                rota_do_usuario.groups.add(grupo)
                form.send_mail()

                messages.success(request, 'Usuário salvo com sucesso. Acesse o seu e-mail para confirmá-lo')
                form = UsuarioComumForm()
            else:
                messages.error(request, 'CPF inválido')
        else:
            messages.error(request, 'Erro ao salvar usuário')
    else:
        form = UsuarioComumForm()  # Senão tiver dados, fica esperando o cliente informa os  dados
        instituicoes = Instituicoes.objects.all()
        print(instituicoes)
    context = {
        'form': form,
        'instituicoes': instituicoes
    }
    return render(request, 'usuario.html', context)


def validar_email_usuario(request):
    if str(request.method) == 'POST':  # Verifica se é o formulário ja tem dados a serem submetidos.
        form = ValidarCadastroUsuario(request.POST, request.FILES)
        if form.is_valid():  # Se sim, valida os dados aqui
            # email_do_cadastro = get_object_or_404(UsuarioComum, email=form.data['validar_email'])
            # email_do_cadastro.campo = True
            # email_do_cadastro.save()
            codigo_de_comparacao = get_object_or_404(UsuarioComum, codigo=form.data['codigo'])
            codigo_de_comparacao.campo = True
            codigo_de_comparacao.save()

            messages.success(request, 'E-mail confirmado com sucesso.')
            form = ValidarCadastroUsuario()
        else:
            messages.error(request, 'Erro ao confirma o e-mail')
    else:
        form = ValidarCadastroUsuario()  # Senão tiver dados, fica esperando o cliente informa os  dados.

    context = {
        'form': form
    }
    return render(request, 'validar_email_usuario.html', context)
