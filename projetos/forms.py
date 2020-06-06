"""Formulário para adicionar projeto"""

from django import forms
from .models import Projetos, Arquivo


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projetos
        fields = ('pro_titulo',
                  'pro_imagem',
                  'pro_desc',
                  'pro_inst',
                  'pro_financiamento',
                  'pro_financiadora')


class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('arq_imagem',
                  'arq_localizacao_documento',
                  'arq_nome',
                  'arq_desc',)
