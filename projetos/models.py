""" Arquivo para criar as classes que persistem no banco de dados.

P/ FAZER:
            Ver uma forma de apresentar o campo pro_financiadora (precisa analisar)
            Ver uma forma de apresentar os nomes das instituições e não os ids no formulário de cadastro
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Este próximo import vai importar modelos do app usuario.
from usuario.models import Pessoa


class Instituicao(models.Model):
    inst_nome = models.CharField(max_length=100)


class Projetos(models.Model):
    FINANCIAMENTO_CHOICES = (
        ("S", "Sim"),
        ("N", "Não")
    )  #
    pro_titulo = models.CharField('Título do projeto:', max_length=100)
    pro_imagem = StdImageField('Imagem:', upload_to='imagem_projeto', null=True)
    pro_desc = models.TextField('Descrição:')
    pro_financiamento = models.CharField('Financiamento:', max_length=1, choices=FINANCIAMENTO_CHOICES, blank=False,
                                         null=False)
    pro_financiadora = models.CharField('Instituição financiadora:', max_length=100)
    pro_datetime = models.DateTimeField('Data de publicação:', blank=True, null=True)
    pro_inst = models.ForeignKey(Instituicao, on_delete=models.CASCADE, null=True)
    pro_usuarios = models.ManyToManyField(
        Pessoa,
        through='ProjetosDosUsuarios',
        through_fields=('pdu_projetos', 'pdu_usuarios'),  #
    )

    def publicar(self):
        self.pro_datetime = timezone.now()
        self.save()

    def __str__(self):
        return self.pro_titulo


class ProjetosDosUsuarios(models.Model):
    pdu_projetos = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    pdu_usuarios = models.ForeignKey(Pessoa, on_delete=models.CASCADE)


class Arquivo(models.Model):
    arq_pro_id = models.ForeignKey(Projetos, on_delete=models.CASCADE, null=True)  # Pegando o id da tabela Projetos
    arq_usu_id = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)  # Pegando o id da tabela Usuarios
    arq_desc = models.TextField('Descrição:')
    arq_nome = models.CharField('Nome:', max_length=100, null=True)
    arq_imagem = StdImageField('Imagem:', upload_to='imagem_projeto_arq', null=True)
    arq_localizacao_documento = RichTextUploadingField( null=True, max_length=1000)
