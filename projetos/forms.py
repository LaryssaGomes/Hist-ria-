from django import forms
from .models import Projetos, Arquivo, Audio, Fotos, Video, Documento, PatrimonioCultura

class PatrimonioCulturaForm(forms.ModelForm):
    class Meta:
        model = PatrimonioCultura
        fields = ('pc_oficio',
                  'pc_expressao',
                  'pc_lugares',
                  'pc_edificacoes',
                  'pc_celebracoes',)

class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('aud_duracao',
                  'aud_audio',)

class FotosForm(forms.ModelForm):
    class Meta:
        model = Fotos
        fields = ('fot_imagem',
                  'fot_tamanho')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('vid_duracao',
                  'vid_video')

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('doc_documento',
                  'doc_numero_de_paginas')

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
        fields = ('arq_colecao',
                  'arq_assunto',
                  'arq_nome',
                  'arq_nivel_de_acesso',
                  'arq_destinatario',
                  'arq_emitente',
                  'arq_texto',
                  'arq_cargo_des',
                  'arq_cargo_emi',
                  'arq_cdd',
                  'arq_idioma',
                  'arq_custodia',
                  'arq_autenticacao',
                  'arq_localizacao_do_acervo',
                  'arq_local_emissao',
                  'arq_tipo_de_formato',
                  'arq_estado',
                  'arq_cidade')
