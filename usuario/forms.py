from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Pessoa, Pesquisador, Bolsista


class CustomUsuarioCreateForm(UserCreationForm):  # Esse é o formulario para adicionar novos usuários

    class Meta:
        model = Pessoa
        fields = ('nome',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Pessoa
        fields = ('nome',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')


class PesquisadorForm(UserCreationForm):

    class Meta:
        model = Pesquisador
        fields = ('nome',
                  'vinculacao',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')
        labels = {'username': 'Username/E-mail'}

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            # user.email = self.cleaned_data["username"]
            if commit:
                user.save()
            return user


class BolsistaForm(UserCreationForm):

    class Meta:
        model = Bolsista
        fields = ('nome',
                  'orientador',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')
        labels = {'username': 'Username/E-mail'}

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            # user.email = self.cleaned_data["username"]
            if commit:
                user.save()
            return user

class Bolsista1Form(forms.ModelForm):

    class Meta:
        model = Bolsista
        fields = ('nome',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')

class Pesquisador1Form(forms.ModelForm):

    class Meta:
        model = Pesquisador
        fields = ('nome',
                  'vinculacao',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')