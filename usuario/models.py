from django.db import models
from stdimage.models import StdImageField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.conf import settings



class UsuarioManager(BaseUserManager):  # Essa é a classe é responsável pela administração dos usuários

    use_in_migrations = True

    """ Essa é classe comum para os dois tipos de usuários (Usuário comum e superUsuário)."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    """ Essa função expecifica as permissões do usuário comum"""

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):  # Essa função expecifica as permissões do superUsuário
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)



class Instituicoes(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sigla = models.CharField('Sigla', max_length=10)
    cidade = models.CharField('Cidade', max_length=70)
    estado = models.CharField('Estado', max_length=50)
    NATUREZA = (
        ('PU', 'Público'),
        ('PR', 'Privado')
    )
    natureza = models.CharField('Natureza', max_length=2, choices=NATUREZA, null=True)
    TIPO_DE_INSTITUICAO = (
        ('EN', 'Ensino'),
        ('CD', 'Centro de Documentação'),
        ('CA', 'Cartório')

    )
    tipo_de_instituicao = models.CharField('Tipo de instituição', max_length=3, choices=TIPO_DE_INSTITUICAO, null=True)
    TIPO_DE_PODER = (
        ('EXE', 'Executivo'),
        ('LEG', 'Legislativo'),
        ('JUD', 'Judiciário'),
        ('PR', 'Privado')
    )
    tipo_de_poder = models.CharField('Tipo de poder', max_length=4, choices=TIPO_DE_PODER, null=True)

    REQUIRED_FIELDS = ['nome', 'cidade', 'estado', 'natureza', 'tipo_de_instituicao', 'tipo_de_poder']

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', unique=True)

    USERNAME_FIELD = 'email'  # Aqui eu estou falando que o email vai ser usado no lugar do nome, para fazer login.
    # Estes seguintes dados serão passados para gerar o formulário.
    REQUIRED_FIELDS = ['nome']


    def __str__(self):
        return self.email  # Retorna o email pois usaremos ele para fazer o login

    objects = UsuarioManager()  # Basicamente esta usando o adminstrador de usuários criado acima.



class UsuarioComum(Usuario):
    # instituicao = models.CharField('Instituição de ensino', max_length=200)
    # O models.PROTECT Cancela a exclusão do registro relacionado se houver relacionamento.
    # instituicao = models.OneToOneField(Instituicoes, on_delete=models.PROTECT)
    salvar_instituicao = models.CharField('Instituição', max_length=100)
    cpf = models.CharField('CPF', max_length=11)
    rg = models.CharField('RG', max_length=11)
    rg_expedidor = models.CharField('Orgão expedidor', max_length=4)
    lattes = models.TextField('Lattes')
    foto = StdImageField('Foto', upload_to='pesquisador', variations={'thumb': (124, 124)})
    telefone = models.CharField('Telefone', max_length=11)
    validar_email = models.EmailField('E-mail')
    campo = models.BooleanField('Validar E-mail', default=False)
    TIPO_DE_USUARIO = (
        ('PE', 'Pesquisador'),
        ('BO', 'Bolsista')
    )
    tipo_de_usuario = models.CharField(max_length=2, choices=TIPO_DE_USUARIO, null=True)

    USERNAME_FIELD = 'email'  # Aqui eu estou falando que o email vai ser usado no lugar do nome, para fazer login.
    # Estes seguintes dados serão passados para gerar o formulário.
    REQUIRED_FIELDS = ['nome', 'salvar_instituição',
                       'cpf', 'rg', 'rg_expedidor', 'lattes', 'foto',
                       'telefone', 'validar_email', 'campo', 'tipo_usuario']


class Vinculacao(models.Model):
    tipo_vinculacao = models.CharField('Tipo de vinculação', max_length=50)
    matricula = models.CharField('Matricula', max_length=20)
    curso = models.CharField('Curso', max_length=100)
    instituicao = models.ForeignKey(Instituicoes, on_delete=models.PROTECT)
    usuario = models.ForeignKey(UsuarioComum, on_delete=models.PROTECT)

