# Generated by Django 2.2.4 on 2020-08-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0037_auto_20200815_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='arq_custodia',
            field=models.CharField(max_length=100, null=True, verbose_name='Custodia:'),
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='arq_idioma',
            field=models.CharField(max_length=100, null=True, verbose_name='Idioma:'),
        ),
    ]