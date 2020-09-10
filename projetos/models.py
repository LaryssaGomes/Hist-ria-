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

from usuario.models import UsuarioComum


import uuid

def user_directory_path_video_file(instance, filename):
    video = 'video'
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return '{0}/{1}'.format(video, filename)

def user_directory_path_documento_file(instance, filename):
    documento = 'documento'
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return '{0}/{1}'.format(documento, filename)

def user_directory_path_audio_file(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    audio = 'audio'
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return '{0}/{1}'.format(audio, filename)


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

        UsuarioComum,

        through='ProjetosDosUsuarios',
        through_fields=('pdu_projetos', 'pdu_usuarios'),  #
    )

    def publicar(self):
        self.pro_datetime = timezone.now()
        self.save()

    def __str__(self):
        return self.pro_titulo

class Notificacao(models.Model):
    noti_bolsista = models.ForeignKey(UsuarioComum, on_delete=models.CASCADE, null=True, related_name='bolsista')
    noti_pesquisador = models.ForeignKey(UsuarioComum, on_delete=models.CASCADE, null=True, related_name='pesquisador')
    noti_arquivo = models.ForeignKey(Projetos, on_delete=models.CASCADE, null=True)

class ProjetosDosUsuarios(models.Model):
    pdu_projetos = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    pdu_usuarios = models.ForeignKey(UsuarioComum, on_delete=models.CASCADE)



class TiposDeDocumento(models.Model):
    tdd_geral = models.CharField('Tipo de Documento Geral:', max_length=100, null=True)
    tdd_especifico = models.CharField('Tipo de Documento Especifico:', max_length=100, null=True, blank=True)

class Arquivo(models.Model):
    arq_tdd_id = models.ForeignKey(TiposDeDocumento, on_delete=models.CASCADE, null=True)
    arq_pro_id = models.ForeignKey(Projetos, on_delete=models.CASCADE, null=True)  # Pegando o id da tabela Projetos
    arq_colecao = models.CharField('Colecao:', max_length=100, null=True, blank=True)
    NIVEL_DE_ACESSO = (
        ('PU', 'Publico'),
        ('PR', 'Privado'),
    )
    arq_nivel_de_acesso = models.CharField('Nivel de acesso:',max_length=2, choices=NIVEL_DE_ACESSO, null=True)
    arq_assunto = models.CharField('Assunto:', max_length=100, null=True)
    arq_cargo_des = models.CharField('Cargo de Destinatario:', max_length=100, null=True, blank=True)
    arq_cargo_emi = models.CharField('Cargo de Emitente:', max_length=100, null=True, blank=True)
    arq_local_emissao = models.CharField('Local Emissao:', max_length=200, blank=True, null=True)
    arq_custodia = models.CharField('Instituição de Custodia:', max_length=100, null=True)
    arq_idioma = models.CharField('Idioma:', max_length=100, null=True)
    arq_cdd = models.DecimalField('Numero de CDD:', max_digits=6, decimal_places=0, blank=True, null=True,)
    '''
    TIPO_DE_DOCUMENTO = (
        ('Documentos Pessoais', (
            ('DPI', 'Identidade'),
            ('DPCN', 'Certidão de nascimento'),
            ('DPCB', 'Certidão de batismo'),
            ('DPCC', 'Certidão de casamento'),
            ('DPCO', 'Certidão de óbito'),
        )
        ),
        ('Pessoais', (
                ('PC', 'Correspondência'),
                ('PD', 'Diário'),
                ('PA', 'Anotação'),
                ('PRC', 'Receita de comida'),
                ('PDM', 'Documento médico'),
            )
        ),
        ('Jurídicos', (
                ('JP', 'Processo'),
                ('JT', 'Testamento'),
                ('JI', 'Inventário'),
                ('JD', 'Depoimento'),
                ('JDs', 'Despacho'),
                ('JS', 'Sentença'),
                ('JA', 'Acórdão'),
            )
        ),
        ('Governamentais', (
                ('GR', 'Relatório'),
                ('GA', 'Ata'),
                ('GL', 'Lei'),
                ('GR', 'Resolução'),
                ('GD', 'Decreto'),
                ('GC', 'Constituição'),
                ('GLs', 'Listas'),
                ('GRI', 'Registro de imóvel'),
                ('GRA', 'Registro de cobrança'),
                ('GRT', 'Registro de trabalho'),
                ('GCA', 'Carta de alforria'),
                ('GRCV', 'Recibo de compra e venda'),
                ('GAp', 'Apólice'),
            )
        ),
        ('Relatos', (
                ('RD', 'Depoimento'),
                ('RE', 'Entrevista'),
                ('RR', 'Relato'),
                ('RM', 'Música'),
            )
        ),
        ('Iconográficos', (
                ('IF', 'Fotografia'),
                ('ID', 'Desenho'),
                ('IM', 'Mapa'),
                ('IP', 'Pintura'),
                ('IC', 'Charge'),
                ('IP', 'Planta'),
            )
        ),
        ('Impressos', (
                ('IJ', 'Jornal'),
                ('IB', 'Boletim'),
                ('IPn', 'Panfleto'),
                ('IPr', 'Propaganda'),
                ('IR', 'Revista'),
                ('IHQ', 'História em quadrinho'),
                ('IL', 'Livro'),
                ('IFl', 'Folder'),
                ('ICr', 'Cardápio'),
                ('IPs', 'Poesia'),
            )
        ),
        ('Vídeos', (
                ('VF', 'Filme'),
                ('VD', 'Documentário'),
                ('VP', 'Propaganda'),
                ('VDs', 'Desenho'),
            )
        ),
   
    )
    '''
    arq_destinatario = models.CharField('Destinatario:',max_length=200, null=True, blank=True)
    arq_emitente = models.CharField('Emitente:',max_length=200, null=True, blank=True)
    arq_estado = models.CharField('Estado',max_length=20, null=True, blank=True)
    arq_cidade = models.CharField('Cidade',max_length=20, null=True, blank=True)
    arq_data = models.CharField('Data', null=True, blank=True, max_length=10)
    arq_data_de_registro = models.DateTimeField('Data de publicação:', blank=True, null=True)
    arq_nome = models.CharField('Titulo:', max_length=100, null=True)
    arq_localizacao_do_acervo = models.CharField('Localização do acervo:', max_length=100, null=True)
    AUTENTICACAO = (
        ('O', 'Original'),
        ('C', 'Copia'),
    )
    arq_autenticacao = models.CharField('Autenticação:',max_length=1, choices=AUTENTICACAO, null=True)
    arq_tipo_de_formato = models.CharField('Tipo de Formato:',max_length=10, null=True)
    arq_texto = RichTextUploadingField( null=True, max_length=1000, blank=True) 
    
class PalavrasChave(models.Model):
    pc_arq = models.ForeignKey(Arquivo, on_delete=models.CASCADE, null=True )
    pc_palavras_chaves = models.CharField('Palavras chaves:',max_length=200, null=True)

class Audio(models.Model):
    aud_arq = models.OneToOneField(Arquivo, on_delete=models.CASCADE, null=True)
    aud_duracao = models.DurationField('Duração:', null=True, blank=True)
    aud_audio = models.FileField('Audio',upload_to=user_directory_path_audio_file,null=True, blank=True)

class Fotos(models.Model):
    fot_arq = models.OneToOneField(Arquivo, on_delete=models.CASCADE, null=True)
    fot_tamanho = models.CharField('Tamanho:',null=True, blank=True, max_length=100)
    fot_imagem = StdImageField('Imagem:', upload_to='imagem_projeto_arq', null=True, blank=True)

class Video(models.Model):
    vid_arq = models.OneToOneField(Arquivo, on_delete=models.CASCADE, null=True)
    vid_video = models.FileField('Video:',upload_to=user_directory_path_video_file,null=True, blank=True)
    vid_duracao = models.DurationField('Duração:', null=True, blank=True)
    
class Documento(models.Model):
    doc_arq = models.OneToOneField(Arquivo, on_delete=models.CASCADE, null=True)
    doc_documento = models.FileField('Documento',upload_to=user_directory_path_documento_file,null=True,blank=True)
    doc_numero_de_paginas = models.DecimalField('Numero de Paginas:', max_digits=3000, decimal_places=0, blank=True, null=True,)

class PatrimonioCultura(models.Model):
    pc_arq = models.OneToOneField(Arquivo, on_delete=models.CASCADE, null=True, blank=True)
    pc_oficio = models.TextField('Oficio:', max_length=100, null=True, blank=True)
    pc_expressao = models.TextField('Formas de expressão:', max_length=100, null=True, blank=True)
    pc_lugares = models.TextField('Lugares:', max_length=100, null=True, blank=True)
    pc_celebracoes = models.TextField('Celebrações', max_length=100, null=True, blank=True)
    pc_edificacoes = models.TextField('Edificações', max_length=100, null=True, blank=True)