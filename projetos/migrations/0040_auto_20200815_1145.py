# Generated by Django 2.2.4 on 2020-08-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0039_auto_20200815_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='arq_colecao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Colecao:'),
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='arq_custodia',
            field=models.CharField(max_length=100, null=True, verbose_name='Instituição de Custodia:'),
        ),
    ]