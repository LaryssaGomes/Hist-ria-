
from typing import Dict

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioComum
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from pycpfcnpj import cpf
# from django.contrib.localflavor.br.forms import BRCPFField
from django.shortcuts import render



class CustomUsuarioCreateForm(UserCreationForm):  # Esse é o formulario para adicionar novos usuários

    class Meta:

        model = UsuarioComum
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


    # cpf = BRCPFField()

    class Meta:
        model = UsuarioComum
        fields = ('nome',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email')



class UsuarioComumForm(UserCreationForm):
    class Meta:
        model = UsuarioComum
        fields = ('nome',
                  # 'instituicao',
                  'salvar_instituicao',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email',
                  'tipo_de_usuario')

        labels = {'username': 'Username/E-mail'}

    def send_mail(self):
        email = self.cleaned_data['email']
        # conteudo = 'Aperte para confirmar o seu email'

        mail = EmailMessage(
            subject='Verificação de e-mail',  # Assunto da messagem
            # Conteudo da menssagem:
            body='Aperte para confirmar o seu email: http://127.0.0.1:8000/cadastro/validar_email_pesquisador/',
            from_email='contatohemeroteca@gmail.com',  # O e-mail de quem está enviando
            to=['contatohemeroteca@gmail.com', ],  # E-mail de destino da messagem
            headers={'reply-to': email}  # Remetente
        )
        mail.send()


class ValidarCadastroUsuario(forms.ModelForm):
    class Meta:
        model = UsuarioComum
        fields = ('validar_email', 'campo')

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioComum
        fields = ('nome',
                  'salvar_instituicao',
                  'cpf',
                  'rg',
                  'rg_expedidor',
                  'lattes',
                  'foto',
                  'telefone',
                  'email',)

