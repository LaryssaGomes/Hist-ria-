"""from django.db import models
from stdimage.models import StdImageField

#SIGNALS
#from django.db.models import signals
from django.template.defaultfilters import slugify

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager): # Essa é a classe é responsável pela administração dos usuários

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields): # Essa é classe comum para os dois tipos de usuários (Usuário comum e superUsuário).
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields): # Essa função expecifica as permissões do usuário comum
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields): # Essa função expecifica as permissões do superUsuário
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    #def adicionarPesquisador():    
        
        #Nessa parte vai ter uma função que permita a entrada do pesquisador.

class Pessoa(AbstractUser): #Esse é o modelo de dados para o pesquisador (ainda é um protótipo) ele é herdado no arquivo forms.py que cria um modelo de formulario e envia para views, para que possa ser passado para o cliente por meio de umm template
    nome = models.CharField('Nome', max_length=100)
    instituicao = models.CharField('Instituição de ensino', max_length=200)
    cpf = models.CharField('CPF', max_length=11)
    rg = models.CharField('RG', max_length=11)
    rg_expedidor = models.CharField('Orgão expedidor', max_length=4)
    lattes = models.TextField('Lattes')
    foto = StdImageField('Foto', upload_to='pesquisador', variations={'thumb': (124, 124)})
    email = models.EmailField('E-mail', unique=True)
    telefone = models.CharField('Telefone', max_length=11)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)
    
    USERNAME_FIELD = 'email' #Aqui eu estou falando que o email vai ser usado no lugar do nome, para fazer login
    REQUIRED_FIELDS = ['nome', 'instituicao', 'cpf', 'rg', 'rg_expedidor', 'lattes', 'foto', 'telefone', 'slug'] # estes serao os dados passados para gerar o formulario


    def __str__(self):
        return self.email #Retorna o email pois usaremos ele para fazer o login
    
    objects = UsuarioManager() #Basicamente esta usando o adminstrador de usuários criado acima"""
