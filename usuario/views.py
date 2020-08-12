from django.shortcuts import render, get_object_or_404
from .forms import UsuarioComumForm, ValidarCadastroUsuario
from django.contrib import messages
from .models import UsuarioComum, Instituicoes


def usuario(request):
    """
    # View do pesquisador, responsável por verificar se o formulario está vazio
    # ou não, validar os dados e salvar no banco.
    """

    if str(request.method) == 'POST':  # Verifica se é o formulário ja tem dados a serem submetidos.
        form = UsuarioComumForm(request.POST, request.FILES)
        instituicoes = Instituicoes.objects.all()
        instituicao_id = request.POST.get('nome_instituicao')
        print(f'olha aqui!!! {instituicao_id}')
        new_form = form.save(commit=False)

        if form.is_valid():
            user = form.save(commit=False)
            user.salvar_instituicao = instituicao_id
            user.username = form.cleaned_data['email']

            form.save()  # Salva os dados
            form.send_mail()

            messages.success(request, 'Usuário salvo com sucesso. Acesse o seu e-mail para confirmá-lo')
            form = UsuarioComumForm()
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
            email_do_cadastro = get_object_or_404(UsuarioComum, email=form.data['validar_email'])
            email_do_cadastro.campo = True
            email_do_cadastro.save()

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
