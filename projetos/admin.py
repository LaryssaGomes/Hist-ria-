
from django.contrib import admin
from .models import (Instituicao,
                     Projetos,
                     ProjetosDosUsuarios,
                     Arquivo,
                     Audio, 
                     Fotos, 
                     Video, 
                     Documento,
                     PalavrasChave,
                     TiposDeDocumento,
                     PatrimonioCultura,
                     Notificacao,)

class NotificacaoAdmin(admin.ModelAdmin):
    list_display =('noti_bolsista',
                   'noti_pesquisador')


class PatrimonioCulturaAdmin(admin.ModelAdmin):
    list_display = ('pc_oficio', 
                    'pc_expressao')

class TiposDeDocumentoAdmin(admin.ModelAdmin): 
    list_display = ('tdd_geral',
                    'tdd_especifico')

class PalavrasChaveAdmin(admin.ModelAdmin):
    list_display = ('pc_arq',
                    'pc_palavras_chaves')

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('doc_documento',
                    'doc_arq',
                    'doc_numero_de_paginas')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('vid_duracao',
                    'vid_video',
                    'vid_arq')

class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('arq_pro_id',
                    'arq_data',
                    'arq_nome',
                    'arq_estado',
                    'arq_data_de_registro',
                    'arq_destinatario',
                    'arq_autenticacao',
                    'arq_emitente',
                    'arq_texto')
                    


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('pro_titulo',
                    'pro_desc',
                    'pro_inst',
                    'pro_financiamento',
                    'pro_financiadora',
                    'pro_imagem')


# Register your models here.
admin.site.register(Instituicao)
admin.site.register(ProjetosDosUsuarios)
# decidi retirar a tabela do administrador, já que o modelo não tem nenhuma aplicação util ainda
admin.site.register(Arquivo, ArquivoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(PatrimonioCultura, PatrimonioCulturaAdmin)
admin.site.register(TiposDeDocumento, TiposDeDocumentoAdmin)
admin.site.register(PalavrasChave, PalavrasChaveAdmin)
admin.site.register(Documento, DocumentoAdmin)

admin.site.register(Notificacao, NotificacaoAdmin)

admin.site.register(Projetos, ProjetoAdmin)