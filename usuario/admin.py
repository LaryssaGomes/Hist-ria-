from django.contrib import admin
from .models import Pesquisador, Bolsista


class PesquisadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'vinculacao')


class BolsistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'orientador')


admin.site.register(Pesquisador, PesquisadorAdmin)
admin.site.register(Bolsista, BolsistaAdmin)
