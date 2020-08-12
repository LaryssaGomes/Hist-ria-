"""from django.shortcuts import render

from django.contrib import messages

from .forms import CustomUsuarioCreateForm #ContatoForm # Importação dos formulários


def pessoa(request): # View do pesquisador, responsável por verificar se o formulario está vazio ou não, validar os dados e salvar no banco 
    if str(request.method) == 'POST': #verifica se é o formulário ja tem dados a serem submetidos
        form = CustomUsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid(): # Se sim, valida os dados aqui
            pesq = form.save(commit=False)
            pesq.username = form.cleaned_data['email']

            form.save() # Salva os dados

            messages.success(request, 'Pesquisador salvo com sucesso.')
            form = CustomUsuarioCreateForm()
        else:
            messages.error(request, 'Erro ao salvar pesquisador')
    else:
        form = CustomUsuarioCreateForm()# Senão tiver dados, fica esperando o cliente informa os  dados

    context = {
        'form': form 
    }
    return render(request, 'pessoa.html', context)"""
