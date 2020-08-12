from django.contrib import admin
from .models import UsuarioComum, Instituicoes


class UsuarioComumAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'campo', 'salvar_instituicao', 'pk')


class InstituicoesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'cidade', 'estado', 'natureza')


admin.site.register(UsuarioComum, UsuarioComumAdmin)
admin.site.register(Instituicoes, InstituicoesAdmin)

