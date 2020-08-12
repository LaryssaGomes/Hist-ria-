"""from django.contrib import admin

from .models import Administrador, Pessoa


class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'email')

admin.site.register(Administrador)
admin.site.register(Pessoa, PessoaAdmin)"""