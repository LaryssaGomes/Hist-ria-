"""from django import forms

from .models import Pessoa

from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class CustomUsuarioCreateForm(UserCreationForm): # Esse é o formulario para adicionar novos usuários

    class Meta:
        model = Pessoa
        fields = ('nome', 'instituicao', 'cpf', 'rg', 'rg_expedidor', 'lattes', 'foto', 'telefone', 'email')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Pessoa
        fields = ('nome', 'instituicao', 'cpf', 'rg', 'rg_expedidor', 'lattes', 'foto', 'telefone', 'email')"""
        

"""class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    assunto = forms.CharField(label='Assunto', max_length=120)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea()"""
    
