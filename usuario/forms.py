from typing import Dict

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioComum
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from random import randint


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


def sequencia():
    numeros = []
    for i in range(1, 7):
        numeros.append(randint(0, 9))
    return numeros


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
                  'tipo_de_usuario',
                  'codigo')

        labels = {'username': 'Username/E-mail'}

    def send_mail(self):
        e_mail = self.cleaned_data['email']
        usuario = UsuarioComum.objects.get(email=e_mail)
        # conteudo = 'Aperte para confirmar o seu email'

        mail = EmailMessage(
            subject='Verificação de e-mail',  # Assunto da messagem
            # Conteudo da menssagem:
            body=f"""Aperte para confirmar o seu email: http://127.0.0.1:8000/cadastro/validar_email_usuario/
                 Digite esse codigo para fazer a confirmação: {usuario.codigo}""",
            from_email='contatohemeroteca@gmail.com',  # O e-mail de quem está enviando
            to=['contatohemeroteca@gmail.com', ],  # E-mail de destino da messagem
            headers={'reply-to': e_mail}  # Remetente
        )
        mail.send()


class ValidarCadastroUsuario(forms.ModelForm):
    class Meta:
        model = UsuarioComum
        fields = ('codigo',)

