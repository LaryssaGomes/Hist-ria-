from django.contrib import admin
from .models import (Instituicao,
                     Projetos,
                     ProjetosDosUsuarios,
                     Arquivo)


class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('arq_pro_id',
                    'arq_usu_id',
                    'arq_desc',
                    'arq_nome',
                    'arq_imagem',
                    'arq_localizacao_documento')


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
admin.site.register(Projetos, ProjetoAdmin)

