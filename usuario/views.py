from django.shortcuts import render
from .forms import PesquisadorForm, BolsistaForm
from django.contrib import messages


def pesquisador(request):
    """
    # View do pesquisador, responsável por verificar se o formulario está vazio
    # ou não, validar os dados e salvar no banco.
    """
    if str(request.method) == 'POST':  # Verifica se é o formulário ja tem dados a serem submetidos
        form = PesquisadorForm(request.POST, request.FILES)
        if form.is_valid():  # Se sim, valida os dados aqui
            pesq = form.save(commit=False)
            pesq.username = form.cleaned_data['email']

            form.save()  # Salva os dados

            messages.success(request, 'Pesquisador salvo com sucesso.')
            form = PesquisadorForm()
        else:
            messages.error(request, 'Erro ao salvar Pesquisador')
    else:
        form = PesquisadorForm()  # Senão tiver dados, fica esperando o cliente informa os  dados

    context = {
        'form': form
    }
    return render(request, 'pesquisador.html', context)


def bolsista(request):
    """
    # View do pesquisador, responsável por verificar se o formulario está vazio
    # ou não, validar os dados e salvar no banco.
    """
    if str(request.method) == 'POST':  # Verifica se é o formulário ja tem dados a serem submetidos
        form = BolsistaForm(request.POST, request.FILES)
        if form.is_valid():  # Se sim, valida os dados aqui
            bols = form.save(commit=False)
            bols.username = form.cleaned_data['email']

            form.save()  # Salva os dados

            messages.success(request, 'Bolsista salvo com sucesso.')
            form = BolsistaForm()
        else:
            messages.error(request, 'Erro ao salvar Bolsista')
    else:
        form = BolsistaForm()  # Senão tiver dados, fica esperando o cliente informa os  dados

    context = {
        'form': form
    }
    return render(request, 'bolsista.html', context)
