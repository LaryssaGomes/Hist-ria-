from django.shortcuts import render, get_object_or_404

from ..models import  Arquivo


def busca_comum(request):
    arquivo = Arquivo.objects.filter(arq_nivel_de_acesso='PU')
    if arquivo.exists():
        return render(request, 'usuariocomum/busca.html', {'arquivos': arquivo})
    else: 
       
        return render(request, 'usuariocomum/busca.html', )
   
def visualizacao_comum(request, id):  # Da uma olhada nesse argumento 'id' depois
    arquivos = get_object_or_404(Arquivo, pk=id)  # Pegando todos os dados na linha que tem o id passado na url.
    return render(request, 'usuariocomum/resultado_busca.html', {'arquivos': arquivos})
