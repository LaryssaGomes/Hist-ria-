from django import forms
from .models import Projetos, Arquivo, Audio, Fotos, Video, Documento

class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('aud_duracao',
                  'aud_audio',)

class FotosForm(forms.ModelForm):
    class Meta:
        model = Fotos
        fields = ('fot_imagem',)

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
                  'arq_nome',
                  'arq_desc',
                  'arq_assunto',
                  'arq_numero_de_caixa',
                  'arq_nivel_de_acesso',
                  'arq_destinatario',
                  'arq_emitente',
                  'arq_texto')
